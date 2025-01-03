import plotly.express as px
import pandas as pd
import logging

def get_table_from_db(db, Table_Class): #* move func to models_handlers
    try:
        # Fetch all records as objects from the database
        records = db.session.query(Table_Class).all() # printing this uses the __repr__ from the class but it does contain every class, not strings of __repr__

        # Dict gets all attributes from every Class (so all columns) in every row (record)
        # Exclude the SQLAlchemy internal state tracking attribute
        data = [{key: getattr(record, key) for key in record.__dict__ if key != '_sa_instance_state'} for record in records]

        df = pd.DataFrame(data)
        return df
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()  # Returns empty DataFrame if there's an error

#todo: put a limit of categories per chart (maybe limit it to the color palette's max amount)
def generate_color_mapping(df, column_name):
    # Get unique categories in the specified column
    categories = df[column_name].unique()
    logging.debug(f"Categories: {categories}")
    # Generate color mapping dictionary
    color_mapping = {}
    for i, category in enumerate(categories):
        # Use a predefined color palette or generate colors dynamically
        # Here, I'm using a predefined palette for demonstration
        color_mapping[category] = px.colors.qualitative.Dark2[i % len(px.colors.qualitative.Dark2)]
    return color_mapping

def generate_bar_chart(df, column_name):
    color_mapping = generate_color_mapping(df, column_name)

    # Plotly won't let you sort data directly, so you need to create a sorted DataFrame first
    result_df = df.groupby(column_name).size().to_frame(name='Counts').sort_values(by='Counts', ascending=False).reset_index()

    fig = px.bar(result_df, x=column_name, y='Counts', 
                 template='plotly_dark', color=column_name, color_discrete_map=color_mapping)

    fig.update_layout(
        xaxis_title=column_name.capitalize(),
        title = f"Users' Tracks' {column_name.capitalize()} Total"
    )

    return fig

def generate_line_chart_lyrics(df, column_name):
    color_mapping = generate_color_mapping(df, column_name)
    date_column = 'lyrics_date_added'

    # Convert date_column to datetime format
    df[date_column] = pd.to_datetime(df[date_column])
    df[date_column] = df[date_column].dt.date # Abstract to day level
    
    pivot_df = df.pivot_table(index=date_column, columns=column_name, aggfunc='size', fill_value=0) #create number of occurences of lang on a given day
    cumsum_df = pivot_df.cumsum()
    fig = px.line(cumsum_df, template='plotly_dark', color_discrete_map=color_mapping)

    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Cumulative Counts',
        title = f"Users' Tracks' {column_name.capitalize()} Trends",
    )

    return fig

def generate_fig_html(fig):
    return fig.to_html(full_html=False)

if __name__ == '__main__':
    get_table_from_db()