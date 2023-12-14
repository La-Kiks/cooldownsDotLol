from flask import Blueprint, render_template, request
import pandas as pd
from back.my_dataframe import champ_dataframe, format_numbers

og_df = champ_dataframe()

views = Blueprint('views', __name__)


@views.route('/',  methods=['GET', 'POST'])
def display_dataframe():
    nbs_columns = [3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 21, 22, 23]
    global og_df  # Access the global DataFrame

    if request.method == 'POST':
        df = og_df.copy()
        haste = float(request.form['haste'])

        # Tricks to apply my maths to the numerical columns
        for my_col in nbs_columns:
            num_col = df.columns[df.columns == df.columns[my_col]]
            df[num_col] = df[num_col].apply(pd.to_numeric, errors='coerce')
            df[num_col] = df[num_col] * (100 / (100 + haste))
            df[num_col] = df[num_col].round(2).map(format_numbers)

        # escape=False is used to proc the html code within the dataframe
        return render_template('base.html',
                               dataframe=df.to_html(escape=False, index=False,
                                                    classes='table-style', table_id='myTable'),
                               haste_value=int(haste),
                               show_form=True)

    return render_template('base.html',
                           dataframe=og_df.to_html(escape=False, index=False,
                                                   classes='table-style', table_id='myTable'),
                           haste_value='',
                           show_form=True)
