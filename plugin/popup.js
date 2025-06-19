// popup.js

document.addEventListener('DOMContentLoaded', async () => {
  const outputDiv = document.getElementById('output');
  const API_KEY = 'YOUR_API_KEY'; // Replace with your actual YouTube Data API key
  const API_URL = 'http://my-elb-2062136355.us-east-1.elb.amazonaws.com:80';

  // Show loading animation initially
  outputDiv.innerHTML = `
      <div class="loading">
        <div class="loading-dot"></div>
        <div class="loading-dot"></div>
        <div class="loading-dot"></div>
      </div>
    `;

  // Get the current tab's URL
  chrome.tabs.query({ active: true, currentWindow: true }, async tabs => {
    const url = tabs[0].url;
    const youtubeRegex =
      /^https:\/\/(?:www\.)?youtube\.com\/watch\?v=([\w-]{11})/;
    const match = url.match(youtubeRegex);

    if (match && match[1]) {
      const videoId = match[1];

      // Update UI with video information
      outputDiv.innerHTML = `
          <div class="section">
            <div class="section-title">Analyzing YouTube Video</div>
            <p>Video ID: ${videoId}</p>
            <p>Fetching comments...</p>
          </div>
        `;

      const comments = await fetchComments(videoId);
      if (comments.length === 0) {
        outputDiv.innerHTML += `<div class="section"><p>No comments found for this video.</p></div>`;
        return;
      }

      outputDiv.innerHTML += `<p>Fetched ${comments.length} comments. Performing sentiment analysis...</p>`;
      const predictions = await getSentimentPredictions(comments);

      if (predictions) {
        // Process the predictions to get sentiment counts and sentiment data
        const sentimentCounts = { 1: 0, 0: 0, '-1': 0 };
        const sentimentData = []; // For trend graph
        const totalSentimentScore = predictions.reduce(
          (sum, item) => sum + parseInt(item.sentiment),
          0
        );
        predictions.forEach((item, index) => {
          sentimentCounts[item.sentiment]++;
          sentimentData.push({
            timestamp: item.timestamp,
            sentiment: parseInt(item.sentiment),
          });
        });

        // Compute metrics
        const totalComments = comments.length;
        const uniqueCommenters = new Set(
          comments.map(comment => comment.authorId)
        ).size;
        const totalWords = comments.reduce(
          (sum, comment) =>
            sum +
            comment.text.split(/\s+/).filter(word => word.length > 0).length,
          0
        );
        const avgWordLength = (totalWords / totalComments).toFixed(2);
        const avgSentimentScore = (totalSentimentScore / totalComments).toFixed(
          2
        );

        // Normalize the average sentiment score to a scale of 0 to 10
        const normalizedSentimentScore = (
          ((parseFloat(avgSentimentScore) + 1) / 2) *
          10
        ).toFixed(2);

        // Add the Comment Analysis Summary section
        outputDiv.innerHTML += `
            <div class="section">
              <div class="section-title">Comment Analysis Summary</div>
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
                  <div class="metric-title">Avg Comment Length</div>
                  <div class="metric-value">${avgWordLength} words</div>
                </div>
                <div class="metric">
                  <div class="metric-title">Avg Sentiment Score</div>
                  <div class="metric-value">${normalizedSentimentScore}/10</div>
                </div>
              </div>
            </div>
          `;

        // Add the Sentiment Analysis Results section with a placeholder for the chart
        outputDiv.innerHTML += `
            <div class="section">
              <div class="section-title">Sentiment Analysis Results</div>
              <div id="chart-container"></div>
            </div>`;

        // Fetch and display the pie chart inside the chart-container div
        await fetchAndDisplayChart(sentimentCounts);

        // Add the Sentiment Trend Graph section
        outputDiv.innerHTML += `
            <div class="section">
              <div class="section-title">Sentiment Trend Over Time</div>
              <div id="trend-graph-container"></div>
            </div>`;

        // Fetch and display the sentiment trend graph
        await fetchAndDisplayTrendGraph(sentimentData);

        // Add the Word Cloud section
        outputDiv.innerHTML += `
            <div class="section">
              <div class="section-title">Comment Wordcloud</div>
              <div id="wordcloud-container"></div>
            </div>`;

        // Fetch and display the word cloud inside the wordcloud-container div
        await fetchAndDisplayWordCloud(comments.map(comment => comment.text));

        // Add the top comments section - UPDATED FOR MODERN DESIGN
        outputDiv.innerHTML += `
            <div class="section">
              <div class="section-title">Top Comments</div>
              <ul class="comment-list">
                ${predictions
                  .slice(0, 25)
                  .map((item, index) => {
                    const sentimentClass = getSentimentClass(item.sentiment);
                    const sentimentText = getSentimentText(item.sentiment);
                    const author =
                      comments[index]?.authorDisplayName || 'Unknown';

                    return `
                  <li class="comment-item ${sentimentClass}">
                    <div class="comment-author">${author}</div>
                    <div class="comment-content">${item.comment}</div>
                    <span class="comment-sentiment">${sentimentText}</span>
                  </li>`;
                  })
                  .join('')}
              </ul>
            </div>
            <div class="footer">
              Analysis completed at ${new Date().toLocaleTimeString([], {
                hour: '2-digit',
                minute: '2-digit',
              })}
            </div>`;
      }
    } else {
      outputDiv.innerHTML = `<div class="section"><p>Please open a YouTube video page first.</p></div>`;
    }
  });

  // Helper functions for sentiment display
  function getSentimentClass(sentiment) {
    switch (sentiment) {
      case '1':
        return 'positive';
      case '0':
        return 'neutral';
      case '-1':
        return 'negative';
      default:
        return '';
    }
  }

  function getSentimentText(sentiment) {
    switch (sentiment) {
      case '1':
        return 'Positive';
      case '0':
        return 'Neutral';
      case '-1':
        return 'Negative';
      default:
        return 'Unknown';
    }
  }

  async function fetchComments(videoId) {
    let comments = [];
    let pageToken = '';
    try {
      while (comments.length < 500) {
        const response = await fetch(
          `https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId=${videoId}&maxResults=100&pageToken=${pageToken}&key=${API_KEY}`
        );
        const data = await response.json();
        if (data.items) {
          data.items.forEach(item => {
            const commentText =
              item.snippet.topLevelComment.snippet.textOriginal;
            const timestamp = item.snippet.topLevelComment.snippet.publishedAt;
            const authorId =
              item.snippet.topLevelComment.snippet.authorChannelId?.value ||
              'Unknown';
            const authorDisplayName =
              item.snippet.topLevelComment.snippet.authorDisplayName ||
              'Unknown';
            comments.push({
              text: commentText,
              timestamp: timestamp,
              authorId: authorId,
              authorDisplayName: authorDisplayName,
            });
          });
        }
        pageToken = data.nextPageToken;
        if (!pageToken) break;
      }
    } catch (error) {
      console.error('Error fetching comments:', error);
      outputDiv.innerHTML += '<p>Error fetching comments.</p>';
    }
    return comments;
  }

  async function getSentimentPredictions(comments) {
    try {
      const response = await fetch(`${API_URL}/predict_with_timestamps`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ comments }),
      });
      const result = await response.json();
      if (response.ok) {
        return result; // The result now includes sentiment and timestamp
      } else {
        throw new Error(result.error || 'Error fetching predictions');
      }
    } catch (error) {
      console.error('Error fetching predictions:', error);
      outputDiv.innerHTML += '<p>Error fetching sentiment predictions.</p>';
      return null;
    }
  }

  async function fetchAndDisplayChart(sentimentCounts) {
    try {
      const response = await fetch(`${API_URL}/generate_chart`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sentiment_counts: sentimentCounts }),
      });
      if (!response.ok) {
        throw new Error('Failed to fetch chart image');
      }
      const blob = await response.blob();
      const imgURL = URL.createObjectURL(blob);
      const img = document.createElement('img');
      img.src = imgURL;
      img.style.width = '100%';
      img.style.marginTop = '20px';
      // Append the image to the chart-container div
      const chartContainer = document.getElementById('chart-container');
      chartContainer.appendChild(img);
    } catch (error) {
      console.error('Error fetching chart image:', error);
      outputDiv.innerHTML += '<p>Error fetching chart image.</p>';
    }
  }

  async function fetchAndDisplayWordCloud(comments) {
    try {
      const response = await fetch(`${API_URL}/generate_wordcloud`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ comments }),
      });
      if (!response.ok) {
        throw new Error('Failed to fetch word cloud image');
      }
      const blob = await response.blob();
      const imgURL = URL.createObjectURL(blob);
      const img = document.createElement('img');
      img.src = imgURL;
      img.style.width = '100%';
      img.style.marginTop = '20px';
      // Append the image to the wordcloud-container div
      const wordcloudContainer = document.getElementById('wordcloud-container');
      wordcloudContainer.appendChild(img);
    } catch (error) {
      console.error('Error fetching word cloud image:', error);
      outputDiv.innerHTML += '<p>Error fetching word cloud image.</p>';
    }
  }

  async function fetchAndDisplayTrendGraph(sentimentData) {
    try {
      const response = await fetch(`${API_URL}/generate_trend_graph`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sentiment_data: sentimentData }),
      });
      if (!response.ok) {
        throw new Error('Failed to fetch trend graph image');
      }
      const blob = await response.blob();
      const imgURL = URL.createObjectURL(blob);
      const img = document.createElement('img');
      img.src = imgURL;
      img.style.width = '100%';
      img.style.marginTop = '20px';
      // Append the image to the trend-graph-container div
      const trendGraphContainer = document.getElementById(
        'trend-graph-container'
      );
      trendGraphContainer.appendChild(img);
    } catch (error) {
      console.error('Error fetching trend graph image:', error);
      outputDiv.innerHTML += '<p>Error fetching trend graph image.</p>';
    }
  }
});
