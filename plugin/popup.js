document.addEventListener('DOMContentLoaded', async () => {
  const outputDiv = document.getElementById('output');

  // Create initial loader
  outputDiv.innerHTML = `
    <div class="loader">
      <div class="loader-spinner"></div>
      <p>Initializing analyzer...</p>
    </div>
  `;

  const API_KEY = 'AIzaSyCt79gbhj58XUmDEpKTUEVi3E75e13Pe18'; // Replace with your YouTube API key
  const API_URL = 'https://tube-pluse-api-latest.onrender.com'; // Replace with your backend URL

  chrome.tabs.query({ active: true, currentWindow: true }, async tabs => {
    const url = tabs[0].url;
    const youtubeRegex =
      /^https:\/\/(?:www\.)?youtube\.com\/watch\?v=([\w-]{11})/;
    const match = url.match(youtubeRegex);

    if (match && match[1]) {
      const videoId = match[1];
      outputDiv.innerHTML = `
        <div class="status-message">
          <div class="section-title"><i class="fas fa-video"></i> YouTube Video ID</div>
          <p>${videoId}</p>
          <p><i class="fas fa-sync-alt fa-spin"></i> Fetching comments...</p>
        </div>
      `;

      const comments = await fetchComments(videoId);
      if (comments.length === 0) {
        outputDiv.innerHTML +=
          '<div class="status-message"><i class="fas fa-exclamation-triangle"></i> No comments found for this video.</div>';
        return;
      }

      outputDiv.innerHTML += `
        <div class="status-message">
          <i class="fas fa-check-circle"></i> Fetched ${comments.length} comments
          <p><i class="fas fa-brain fa-spin"></i> Performing sentiment analysis...</p>
        </div>
      `;

      const predictions = await getSentimentPredictions(comments);

      if (predictions) {
        const sentimentCounts = { 1: 0, 0: 0, '-1': 0 };
        const totalSentimentScore = predictions.reduce(
          (sum, item) => sum + parseInt(item.sentiment),
          0
        );

        predictions.forEach(item => {
          sentimentCounts[item.sentiment]++;
        });

        const totalComments = comments.length;
        const uniqueCommenters = new Set(comments.map(c => c.authorId)).size;
        const totalWords = comments.reduce(
          (sum, c) => sum + c.text.split(/\s+/).length,
          0
        );
        const avgWordLength = (totalWords / totalComments).toFixed(2);
        const avgSentimentScore = (totalSentimentScore / totalComments).toFixed(
          2
        );
        const normalizedSentimentScore = (
          ((parseFloat(avgSentimentScore) + 1) / 2) *
          10
        ).toFixed(2);

        // Create metrics HTML
        const metricsHTML = `
          <div class="section">
            <div class="section-title"><i class="fas fa-chart-pie"></i> Analysis Summary</div>
            <div class="metrics-container">
              <div class="metric">
                <div class="metric-title">Total Comments</div>
                <div class="metric-value">${totalComments}</div>
              </div>
              <div class="metric">
                <div class="metric-title">Unique Commenters</div>
                <div class="metric-value">${uniqueCommenters}</div>
              </div>
              <div class="metric">
                <div class="metric-title">Avg. Words</div>
                <div class="metric-value">${avgWordLength}</div>
              </div>
              <div class="metric">
                <div class="metric-title">Sentiment Score</div>
                <div class="metric-value">${normalizedSentimentScore}/10</div>
              </div>
            </div>
          </div>
        `;

        // Create sentiment distribution section
        const sentimentDistributionHTML = `
          <div class="section">
            <div class="section-title"><i class="fas fa-chart-bar"></i> Sentiment Distribution</div>
            <div id="chart-container" class="chart-container">
              <div class="loader">
                <div class="loader-spinner"></div>
                <p>Generating chart...</p>
              </div>
            </div>
          </div>
        `;

        // Create wordcloud section
        const wordcloudHTML = `
          <div class="section">
            <div class="section-title"><i class="fas fa-cloud"></i> Comment Wordcloud</div>
            <div id="wordcloud-container" class="wordcloud-container">
              <div class="loader">
                <div class="loader-spinner"></div>
                <p>Generating word cloud...</p>
              </div>
            </div>
          </div>
        `;

        // Create comments section
        const commentsHTML = `
          <div class="section">
            <div class="section-title"><i class="fas fa-comments"></i> Top Comments Analysis</div>
            <ul class="comment-list" id="comment-list">
              ${predictions
                .slice(0, 25)
                .map(
                  (item, i) => `
                <li class="comment-item">
                  <span>${i + 1}. ${truncateText(item.comment, 80)}</span><br>
                  <span class="comment-sentiment sentiment-${getSentimentClass(
                    item.sentiment
                  )}">
                    ${getSentimentIcon(item.sentiment)} ${getSentimentLabel(
                    item.sentiment
                  )}
                  </span>
                </li>`
                )
                .join('')}
            </ul>
          </div>
        `;

        // Combine all sections
        outputDiv.innerHTML =
          metricsHTML +
          sentimentDistributionHTML +
          wordcloudHTML +
          commentsHTML;

        // Generate visualizations
        await fetchAndDisplayChart(sentimentCounts);
        await fetchAndDisplayWordCloud(comments.map(c => c.text));
      }
    } else {
      outputDiv.innerHTML = `
        <div class="status-message">
          <i class="fas fa-exclamation-circle"></i>
          <p>This is not a valid YouTube URL.</p>
          <p>Please open a YouTube video page.</p>
        </div>
      `;
    }
  });

  // Helper functions
  function truncateText(text, maxLength) {
    return text.length > maxLength
      ? text.substring(0, maxLength) + '...'
      : text;
  }

  function getSentimentClass(sentiment) {
    if (sentiment === '1') return 'positive';
    if (sentiment === '0') return 'neutral';
    return 'negative';
  }

  function getSentimentLabel(sentiment) {
    if (sentiment === '1') return 'Positive';
    if (sentiment === '0') return 'Neutral';
    return 'Negative';
  }

  function getSentimentIcon(sentiment) {
    if (sentiment === '1') return '<i class="fas fa-smile"></i>';
    if (sentiment === '0') return '<i class="fas fa-meh"></i>';
    return '<i class="fas fa-frown"></i>';
  }

  async function fetchComments(videoId) {
    let comments = [],
      pageToken = '';
    try {
      while (comments.length < 1000) {
        const res = await fetch(
          `https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId=${videoId}&maxResults=100&pageToken=${pageToken}&key=${API_KEY}`
        );
        const data = await res.json();
        if (data.items) {
          data.items.forEach(item => {
            const snippet = item.snippet.topLevelComment.snippet;
            comments.push({
              text: snippet.textOriginal,
              timestamp: snippet.publishedAt,
              authorId: snippet.authorChannelId?.value || 'Unknown',
            });
          });
        }
        pageToken = data.nextPageToken;
        if (!pageToken) break;
      }
    } catch (err) {
      console.error('Error fetching comments:', err);
      outputDiv.innerHTML += '<p>Error fetching comments.</p>';
    }
    return comments;
  }

  async function getSentimentPredictions(comments) {
    try {
      const res = await fetch(`${API_URL}/predict_with_timestamps`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ comments }),
      });
      return await res.json();
    } catch (err) {
      console.error('Error:', err);
      outputDiv.innerHTML += '<p>Error fetching predictions.</p>';
      return null;
    }
  }

  async function fetchAndDisplayChart(sentimentCounts) {
    try {
      const res = await fetch(`${API_URL}/generate_chart`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sentiment_counts: sentimentCounts }),
      });
      const blob = await res.blob();
      const img = document.createElement('img');
      img.src = URL.createObjectURL(blob);
      document.getElementById('chart-container').innerHTML = '';
      document.getElementById('chart-container').appendChild(img);
    } catch (err) {
      console.error('Chart error:', err);
      document.getElementById('chart-container').innerHTML =
        '<p class="status-message">Error fetching chart.</p>';
    }
  }

  async function fetchAndDisplayWordCloud(comments) {
    try {
      const res = await fetch(`${API_URL}/generate_wordcloud`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ comments }),
      });
      const blob = await res.blob();
      const img = document.createElement('img');
      img.src = URL.createObjectURL(blob);
      document.getElementById('wordcloud-container').innerHTML = '';
      document.getElementById('wordcloud-container').appendChild(img);
    } catch (err) {
      console.error('Word cloud error:', err);
      document.getElementById('wordcloud-container').innerHTML =
        '<p class="status-message">Error fetching word cloud.</p>';
    }
  }
});
