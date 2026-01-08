## 🧠 Design Decisions & Strategy

### 1. Chunking Strategy
- **Approach:** Fixed-size character chunking with a window of 1,000 characters.
- **Why?** Since we are using Markdown, 1,000 characters typically cover 2-3 logical paragraphs. This size is small enough to be precise for retrieval but large enough to maintain semantic meaning. We use Markdown format instead of raw text because headers (`#`, `##`) act as natural anchors for the OpenAI File Search tool.

### 2. Delta Sync Mechanism
- **Logic:** We use MD5 hashing to generate a unique fingerprint for each article's content.
- **Efficiency:** On daily runs, the system compares new hashes with the `manifest.json`. Only articles with modified content are re-processed and re-uploaded, significantly reducing OpenAI storage costs and API overhead.

## 🐳 Dockerization & Deployment
The application is containerized to run as a scheduled job (e.g., DigitalOcean Cron Job).

**To run the container locally:**
1. Build: `docker build -t optibot-sync .`
2. Run: `docker run --env-file .env optibot-sync`

The job will:
1. Scrape latest content.
2. Compare hashes.
3. Update OpenAI Vector Store.
4. Exit with code 0.

## 📸 Proof of Work
### Terminal Logs
The system successfully identified 30 articles and calculated 265 semantic chunks. On the second run, the Delta Sync correctly skipped all 30 files as no changes were detected.

### Playground Result
[Add your screenshot here showing the bot's answer with URL citations]

## 📁 Project Structure
- `main.py`: Entry point and orchestration.
- `scraper.py`: Zendesk API integration and HTML-to-Markdown conversion.
- `uploader.py`: OpenAI Vector Store & Files API management.
- `manifest.json`: Persistent state for Delta Sync.
- `Dockerfile`: Container configuration.

## 📝 Execution Note
Due to API quota limits on the personal testing account, the Playground chat interface was restricted. However, the successful integration can be verified via:
1. **Console Logs:** Confirming 30 files processed and 265 semantic chunks created.
2. **OpenAI Dashboard:** As shown in the attached screenshots, the `OptiBot` assistant is correctly configured with the `File Search` tool linked to the synchronized Vector Store containing the processed Markdown documents.

### 🔄 Delta Sync Verification
The system generates a `manifest.json` file to keep track of document versions. 
- **Article ID:** Unique identifier from the source API.
- **Content Hash:** MD5 signature of the Markdown content.

On subsequent runs, the system compares these hashes. If the content hasn't changed, the article is skipped, as shown in the console logs (Added: 0, Skipped: 30). This ensures efficiency and cost-optimization for the OpenAI Vector Store.

### Daily Job Logs
Refer to last_run.log for the latest execution output. System is configured to run daily via Docker on a scheduled platform.