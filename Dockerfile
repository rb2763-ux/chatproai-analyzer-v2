FROM python:3.12-slim

# Cache bust: 2026-01-30-v2
WORKDIR /app

# Install Python deps first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright Chromium + ALL system dependencies in one step
RUN playwright install --with-deps chromium && \
    playwright install-deps && \
    apt-get install -y --no-install-recommends libxfixes3 && \
    rm -rf /var/lib/apt/lists/*

# Verify Chromium works
RUN python -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); b = p.chromium.launch(headless=True, args=['--no-sandbox']); b.close(); p.stop(); print('✅ Chromium works!')"

# Copy app code
COPY . .

# Expose port
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
