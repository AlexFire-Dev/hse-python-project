import pandas as pd
from flask import Flask, render_template, request, redirect


def get_df():
    df = pd.read_csv("dataset/Motor_Vehicle_Collisions.csv")
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.str.lower()

    df = df.drop(columns=[
        'vehicle_type_code_5',
        'contributing_factor_vehicle_5',
        'vehicle_type_code_4',
        'contributing_factor_vehicle_4',
        'vehicle_type_code_3',
        'contributing_factor_vehicle_3',
        'off_street_name',
        'zip_code'
    ])

    df.drop('location', axis=1, inplace=True)

    df = df.dropna()

    df['crash_date'] = pd.to_datetime(df['crash_date'])

    return df


app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# This is to stop force sorting in response, by default jsonify sorts the response keys alphabetically
app.config["JSON_SORT_KEYS"] = False
df = get_df()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analytics')
def analytics():
    return render_template('analytics.html')


@app.route('/interactive', methods=['GET', 'POST'])
def interactive():
    if request.method == 'POST':
        print(request.form)
        date = request.form['date']
        try:
            date = date.split('-')

            if len(date[0]) != 4 or len(date[1]) != 2 or len(date[2]) != 2:
                raise Exception

            date = '/'.join(date)

            dt = df[df["crash_date"] == date]

            res = [f"Number of motorist injured at {date} in {dt.shape[0]} crashes:",
                   f"Mean: {dt['number_of_motorist_injured'].mean()}",
                   f"Median: {(dt['number_of_motorist_injured'].max() + dt['number_of_motorist_injured'].min()) / 2}",
                   f"Standart deviation: {dt['number_of_motorist_injured'].std()}"]

            return render_template('interactive.html', rows=res)
        except:
            res = ['Date format is wrong, it should look like 2023-09-01']
            return render_template('interactive.html', rows=res)
    else:
        return render_template('interactive.html')


@app.route('/notebook')
def notebook():
    return render_template('notebook.html')


@app.route('/streamlit')
def streamlit():
    return render_template('streamlit.html', stlit="http://localhost:8501/")


if __name__ == '__main__':
    app.run(debug=True, port=8500)
