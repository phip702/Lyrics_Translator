import unittest
import pandas as pd
from app.plots import generate_bar_chart, generate_line_chart_lyrics
import unittest.mock
import unittest

def mock_get_table_from_db():
    # Saved testing data set
    return pd.read_csv('./test_data/track_name_artist_detlang_date.csv')

class TestPlots(unittest.TestCase):
    ''' This test will not cover the HTML from the generate_fig_html(fig) function, but that function is just fig.tohtml() so it shouldn't cause problems.'''
    
    def test_generate_bar_chart(self):
        # Read data from CSV file
        df = mock_get_table_from_db()
        
        fig1 = generate_bar_chart(df, 'detected_language')
        fig2 = generate_line_chart_lyrics(df, 'detected_language')
        
        self.assertIsNotNone(fig1, msg = "plot is empty")

        # Get the plot HTML
        plot_html1 = fig1.to_html()
        plot_html2 = fig2.to_html()
        
        # Write the plot HTML to the test_plots.html file
        with open('tests/test_plots1.html', 'w') as f:
            f.write(plot_html1)  

        with open('tests/test_plots2.html', 'w') as f:
            f.write(plot_html2)  

        #* Check the tests_plots_page.html to see what it renders

if __name__ == '__main__':
    unittest.main()
