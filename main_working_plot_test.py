from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.layouts import gridplot
import numpy as np
from bokeh.plotting import figure, show, output_notebook

class PlotSsdSums:
    
    def __init__(self, ssd_sums, test_results):
        self.ssd_sums = ssd_sums
        self.test_results = test_results
    
    def plot(self):
        ssd_sums= self.ssd_sums
        # Function to create a plot for given SSD sums
        def create_ssd_plot(ssd_sums, title):
            # Calculate log10 of SSD values
            ssd_log = np.log10(list(ssd_sums.values()))
            
            # Find the minimum SSD value and its corresponding ideal function
            min_ssd_value = min(ssd_log)
            colors = ['green' if ssd == min_ssd_value else 'lightblue' for ssd in ssd_log]
            
            # Create a ColumnDataSource, now including a color field
            ssd_source_log = ColumnDataSource(data=dict(
                ideal_funcs=list(ssd_sums.keys()),
                ssd=ssd_log,
                colors=colors  # Add color information here
            ))
            
            # Create the figure
            p = figure(x_range=list(ssd_sums.keys()), title=title, width=700, height=350, tools="")
            
            # Draw the bars, setting fill_color to use the colors from the source
            p.vbar(x='ideal_funcs', top='ssd', width=0.9, source=ssd_source_log, line_color='white', fill_color='colors')
            
            # Configure hover tool
            hover = HoverTool()
            hover.tooltips = [
                ("Ideal Function", "@ideal_funcs"),
                ("Log10(SSD)", "@ssd{0,0.00}")
            ]
            p.add_tools(hover)
            
            # Rotate x-axis labels for better visibility
            p.xaxis.major_label_orientation = "vertical"
            
            return p

        ssd_sums_y1 = ssd_sums['Y1 (training func)']
        ssd_sums_y2 = ssd_sums['Y2 (training func)']
        ssd_sums_y3 = ssd_sums['Y3 (training func)']
        ssd_sums_y4 = ssd_sums['Y4 (training func)']

        # Example usage: Print the ideal function with the lowest SSD for Y1 (training func)
        lowest_ssd_y1 = min(ssd_sums_y1, key=ssd_sums_y1.get)
        lowest_ssd_y2 = min(ssd_sums_y2, key=ssd_sums_y2.get)
        lowest_ssd_y3 = min(ssd_sums_y3, key=ssd_sums_y3.get)
        lowest_ssd_y4 = min(ssd_sums_y4, key=ssd_sums_y4.get)
        # Create a plot for each set of SSD sums
        p1 = create_ssd_plot(ssd_sums['Y1 (training func)'], f'SSD for Y1 (training func)-Log Sclae & The Function selected is {lowest_ssd_y1} @Value {ssd_sums_y1[lowest_ssd_y1]}')
        p2 = create_ssd_plot(ssd_sums['Y2 (training func)'], f'SSD for Y1 (training func)-Log Sclae & The Function selected is {lowest_ssd_y2} @Value {ssd_sums_y2[lowest_ssd_y2]}')
        p3 = create_ssd_plot(ssd_sums['Y3 (training func)'], f'SSD for Y1 (training func)-Log Sclae & The Function selected is {lowest_ssd_y3} @Value {ssd_sums_y2[lowest_ssd_y3]}')
        p4 = create_ssd_plot(ssd_sums['Y4 (training func)'], f'SSD for Y1 (training func)-Log Sclae & The Function selected is {lowest_ssd_y4} @Value {ssd_sums_y2[lowest_ssd_y4]}')

        # Arrange the plots in a grid
        grid = gridplot([[p1, p2], [p3, p4]])

        # Show the grid
        show(grid)
    
    def scatter_test_results(self):
        df_test_results = self.test_results

        # Assuming df_test_results is already defined and loaded with data

        # Ensure the notebook output is set correctly
        output_notebook()

        # Generate a random color for each data point
        np.random.seed(42)  # For reproducibility
        colors = ['#' + ''.join([np.random.choice(list('0123456789ABCDEF')) for j in range(6)]) for i in range(len(df_test_results))]

        # Prepare the data
        source = ColumnDataSource(data={
            'x_test': df_test_results['X (test func)'].astype(float),
            'y_test': df_test_results['Y (test func)'].astype(float),
            'ideal_func': df_test_results['No. of ideal func'],
            'delta_y': df_test_results['Delta Y (test func)'],
            'colors': colors  # Add the generated colors to the source
        })

        # Create the figure
        p = figure(width=1000, height=600, title="Test Results Scatter Plot",
                x_axis_label='X (test func)', y_axis_label='Y (test func)',
                tools="pan,wheel_zoom,box_zoom,reset,save")

        # Add a scatter renderer with dynamic coloring
        p.scatter('x_test', 'y_test', color='colors', source=source, size=20, alpha=0.6)

        # Add a hover tool
        hover = HoverTool()
        hover.tooltips = [
            ("X (test func)", "@x_test"),
            ("Y (test func)", "@y_test"),
            ("No. of ideal func", "@ideal_func"),
            ("Delta Y", "@delta_y")
        ]

        p.add_tools(hover)

        # Show the result
        show(p)
    
    
