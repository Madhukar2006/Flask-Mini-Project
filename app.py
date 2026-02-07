from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for tasks (simple list-based CRUD)
# Note: Using global variables for demonstration purposes only.
# Production applications should use proper database storage (SQLite, PostgreSQL, etc.)
tasks = []
task_id_counter = 1


@app.route('/')
def index():
    """Display all tasks (Read operation)"""
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add_task():
    """Handle form submission to add a new task (Create operation)"""
    global task_id_counter
    
    task_name = request.form.get('task_name')
    task_description = request.form.get('task_description')
    
    if task_name:  # Only add if task name is provided
        new_task = {
            'id': task_id_counter,
            'name': task_name,
            'description': task_description or ''
        }
        tasks.append(new_task)
        task_id_counter += 1
    
    return redirect(url_for('index'))


@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    """Edit an existing task (Update operation)"""
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if not task:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # Update task with new data
        task_name = request.form.get('task_name')
        task_description = request.form.get('task_description', '')
        
        # Validate that task name is not empty
        if task_name:
            task['name'] = task_name
            task['description'] = task_description
        
        return redirect(url_for('index'))
    
    # GET request - show edit form
    return render_template('edit.html', task=task)


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """Delete a task (Delete operation)"""
    global tasks
    tasks = [t for t in tasks if t['id'] != task_id]
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Note: debug=True and host='0.0.0.0' are for development only
    # In production, use a proper WSGI server (e.g., Gunicorn) and disable debug mode
    app.run(debug=True, host='0.0.0.0', port=5000)
