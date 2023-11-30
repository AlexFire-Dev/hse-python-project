from flask import Flask, render_template
import streamlit as st


app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# This is to stop force sorting in response, by default jsonify sorts the response keys alphabetically
app.config["JSON_SORT_KEYS"] = False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/notebook')
def notebook():
    return render_template('notebook.html')


@app.route('/streamlit')
def streamlit():
    st.set_page_config(page_title="My Streamlit App")
    st.write("Hello, world!")
    return "hello"


if __name__ == '__main__':
    app.run(debug=True, port=8500)
