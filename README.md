<h1>Library Management Application</h1>
<h4>Backend - Python/Flask</h4>
<h4>Frontend - Vue3.js</h4>
<h4>Backend Jobs - Celery-Redis</h4>
<h4>Cache Management - Redis</h4>
<br>
<h5>Execute the following commands</h5>
<br>
<h5>*************** Initial Setup ***************</h5>
<p>1. cd backend </p>
<p>2. python3 -m venv venv or python -m venv venv </p>
<p>3. source venv/bin/activate </p>
<p>4. pip install -r requirements.txt </p>
<h6>Open new Terminal</h6>
<p>1. cd frontend/libmgmt_app </p>
<p>2. npm install</p>
<br>
<h5>*************** Start Backend ***************</h5>
<p>1. cd backend </p>
<p>2. source venv/bin/activate </p>
<p>3. python3 run.py or python run.py </p>
<br>
<h5>*************** Start Frontend ***************</h5>
<p>1. cd frontend/libmgmt_app </p>
<p>2. npm run serve -- --port 8081 </p>
<br>
<h5>*************** Start Celery Worker ***************</h5>
<p>1. cd backend </p>
<p>2. celery -A tasks worker --loglevel=info </p>
<br>
<h5>*************** Start Celery Scheduler ***************</h5>
<p>1. cd backend </p>
<p>2. celery -A tasks beat --loglevel=info </p>