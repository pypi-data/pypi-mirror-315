import matplotlib.pyplot as plt

colour_cycle = plt.rcParams["axes.prop_cycle"].by_key()['color']

class BarChart:
    def __init__(
        self,
        title: str = "Bar Chart",
        xlabel: str = "Categories",
        ylabel: str = "Values",
        bar_color: str = colour_cycle[0],
        figsize: tuple = (8, 5),
        gridlines: bool = True,
    ) -> None:
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.bar_color = bar_color
        self.figsize = figsize
        self.gridlines = gridlines

        self.categories = []
        self.values = []

    def set_data_from_dict(self, data: dict):
        if not isinstance(data, dict):
            raise TypeError(f"Data must be a dictionary, not {type(data).__name__}.")

        self.categories = list(data.keys())
        self.values = list(data.values())

    def set_data_from_lists(self, categories: list, values: list):
        if not isinstance(categories, list):
            raise TypeError(f"categories must be a list, not {type(categories).__name__}.")

        if not isinstance(values, list):
            raise TypeError(f"values must be a list, not {type(values).__name__}.")

        if len(categories) != len(values):
            raise ValueError("categories and values must have the same length.")

        self.categories = categories
        self.values = values

    def plot(self, save_as: str = None):
        if not self.categories or not self.values:
            raise ValueError("Data is not set. Please set data before plotting.")

        plt.bar(self.categories, self.values, color=self.bar_color)

        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)

        if self.gridlines:
            plt.grid(axis="y", linestyle="-", alpha=0.7)

        if save_as:
            plt.savefig(save_as)
            plt.close()
        else:
            plt.show()
            

class LineGraph:
    def __init__(
        self,
        title: str = "Line Graph",
        xlabel: str = "X Axis",
        ylabel: str = "Y Axis",
        line_color: str = colour_cycle[0],
        line_style: str = "-",
        marker: str = "",
        figsize: tuple = (8, 5),
        gridlines: bool = True,
    ) -> None:
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.line_color = line_color
        self.line_style = line_style
        self.marker = marker
        self.figsize = figsize
        self.gridlines = gridlines

        self.x = []
        self.y = []
        
    def set_data_from_coords(self, coords: list):
        if not isinstance(coords, list):
            raise TypeError("coords must be a dictionary.")
        
        for coord in coords:
            if not isinstance(coord, (tuple, list)):
                raise ValueError(f"Coordinate pair must be a tuple or list, not {type(coord).__name__}.")
            if len(coord) != 2:
                raise ValueError(f"Coordinate pair must have 2 values, not {len(coord)}.")
        
        x_coords, y_coords = zip(*coords)
        self.x = list(x_coords)
        self.y = list(y_coords)

    def set_data_from_lists(self, x: list, y: list):
        if not isinstance(x, list):
            raise TypeError(f"x must be a list, not {type(x).__name__}.")

        if not isinstance(y, list):
            raise TypeError(f"y must be a list, not {type(y).__name__}.")

        if len(x) != len(y):
            raise ValueError("x and y must have the same length.")

        self.x = x
        self.y = y
    
    def plot(self, save_as: str = None):
        if not self.x or not self.y:
            raise ValueError("Data is not set. Please set data before plotting.")

        plt.plot(self.x, self.y, color=self.line_color, linestyle=self.line_style, marker=self.marker)

        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)

        if self.gridlines:
            plt.grid(axis="y", linestyle="-", alpha=0.7)

        if save_as:
            plt.savefig(save_as)
            plt.close()
        else:
            plt.show()

class ScatterPlot:
    def __init__(
        self,
        title: str = "Scatter Plot",
        xlabel: str = "X Axis",
        ylabel: str = "Y Axis",
        marker_color: str = colour_cycle[0],
        marker: str = "o",
        figsize: tuple = (8, 5),
        gridlines: bool = True,
    ) -> None:
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.marker_color = marker_color
        self.marker = marker
        self.figsize = figsize
        self.gridlines = gridlines

        self.x = []
        self.y = []
        
    def set_data_from_coords(self, coords: list):
        if not isinstance(coords, list):
            raise TypeError("coords must be a dictionary.")
        
        for coord in coords:
            if not isinstance(coord, (tuple, list)):
                raise ValueError(f"Coordinate pair must be a tuple or list, not {type(coord).__name__}.")
            if len(coord) != 2:
                raise ValueError(f"Coordinate pair must have 2 values, not {len(coord)}.")
        
        x_coords, y_coords = zip(*coords)
        self.x = list(x_coords)
        self.y = list(y_coords)

    def set_data_from_lists(self, x: list, y: list):
        if not isinstance(x, list):
            raise TypeError(f"x must be a list, not {type(x).__name__}.")

        if not isinstance(y, list):
            raise TypeError(f"y must be a list, not {type(y).__name__}.")

        if len(x) != len(y):
            raise ValueError("x and y must have the same length.")

        self.x = x
        self.y = y
    
    def plot(self, save_as: str = None):
        if not self.x or not self.y:
            raise ValueError("Data is not set. Please set data before plotting.")

        plt.scatter(self.x, self.y, color=self.marker_color, marker=self.marker)

        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)

        if self.gridlines:
            plt.grid(axis="y", linestyle="-", alpha=0.7)

        if save_as:
            plt.savefig(save_as)
            plt.close()
        else:
            plt.show()