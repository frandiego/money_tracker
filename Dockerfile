FROM python:3.9
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8080
COPY . .
CMD streamlit run main.py --server.port 8080
