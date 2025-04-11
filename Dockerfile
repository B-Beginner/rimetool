FROM python:3.10
WORKDIR /app
# Copy dependency files and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
# Copy setup file and the main package directory, then install the package
COPY setup.py /app/
COPY rimetool /app/rimetool
RUN pip install -e .
# Copy all remaining source files
COPY . .
# Expose application port (adjust as needed)
EXPOSE 5001
# Start the application with the designated entry point
CMD ["python", "rimetool/rimetool_gui/new_app.py"]
