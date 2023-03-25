FROM python:3.6

# Create app directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt ./
RUN pip3 install -r requirements.txt --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org

# Copy app source code
COPY . .

# Set Flask environment variables
ENV FLASK_APP=api
ENV FLASK_ENV=production
# ENV FLASK_ENV=development

# Expose port
EXPOSE $PORT

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 ${FLASK_APP}:'create_app()'