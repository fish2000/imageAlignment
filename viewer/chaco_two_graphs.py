#!/usr/bin/env python
# Major library imports
from numpy import cosh, exp, linspace, meshgrid, pi, tanh
from scipy.special import jn

# Enthought library imports
from traits.util.resource import find_resource
from enable.api import Component, ComponentEditor
from traits.api import File, Range, HasTraits, Instance
from traitsui.api import Item, Group, View, Handler
from traitsui.menu \
    import Action, CloseAction, Menu, MenuBar, OKCancelButtons, Separator


# Chaco imports
from chaco.api import ArrayPlotData, HPlotContainer, jet, Plot, PlotGraphicsContext, ImageData
from chaco.tools.api import PanTool, ZoomTool
import os, sys

#===============================================================================
# # Create the Chaco plot.
#===============================================================================
def _create_plot_component():
    pass

#===============================================================================
# Attributes to use for the plot view.
size = (1300, 700)
title = "Line plots with hold"

#===============================================================================
# # Demo class that is used by the demo.py application.
#===============================================================================

def attach_tools(plot):
    #plot.tools.append(PanTool(plot))
    zoom = ZoomTool(component=plot, tool_mode="box", always_on=False)
    plot.overlays.append(zoom)

class Demo(HasTraits):
    pd = Instance(ArrayPlotData, ())
    plot = Instance(HPlotContainer)
    
    _load_file = File(
        find_resource('imageAlignment', '../images/GIRLS-IN-SPACE.jpg',
        '../images/GIRLS-IN-SPACE.jpg', return_path=True))
    _save_file = File
    
    load_file_view = View(
        Item('_load_file'),
        buttons=OKCancelButtons,
        kind='livemodal',
        width=400,
        resizable=True,
    )
    
    save_file_view = View(
        Item('_save_file'),
        buttons=OKCancelButtons,
        kind='livemodal',
        width=400,
        resizable=True,
    )
    
    def __init__(self, *args, **kwargs):
        super(Demo, self).__init__(*args, **kwargs)
        
        from imread import imread
        imarray = imread(find_resource('imageAlignment', '../images/GIRLS-IN-SPACE.jpg',
            '../images/GIRLS-IN-SPACE.jpg', return_path=True))
        
        self.pd = ArrayPlotData(imagedata=imarray)
        #self.pd.x_axis.orientation = "top"
        self.plot = HPlotContainer()
        
        titles = ["I KEEP DANCE", "ING ON MY OWN"]
        
        
        self._load()
        
        i = 0
        for plc in [Plot, Plot]:
            xs = linspace(0, 334*pi, 333)
            ys = linspace(0, 334*pi, 333)
            x, y = meshgrid(xs,ys)
            z = tanh(x*y/6)*cosh(exp(-y**2)*x/3)
            z = x*y
            
            _pd = ArrayPlotData()
            _pd.set_data("drawdata", z)
            _pd.set_data("imagedata", self.pd.get_data('imagedata'))
            
            plc = Plot(_pd,
                title="render_style = hold",
                padding=50, border_visible=True, overlay_border=True)
            
            self.plot.add(plc)
            
            plc.img_plot("imagedata",
                alpha=0.95)
            
            # Create a contour polygon plot of the data
            plc.contour_plot("drawdata",
                              type="poly",
                              poly_cmap=jet,
                              xbounds=(0, 499),
                              ybounds=(0, 582),
                              alpha=0.35)
            
            # Create a contour line plot for the data, too
            plc.contour_plot("drawdata",
                              type="line",
                              xbounds=(0, 499),
                              ybounds=(0, 582),
                              alpha=0.35)
            
            # Create a plot data obect and give it this data
            plc.legend.visible = True
            plc.title = titles[i]
            i += 1
            
            #plc.plot(("index", "y0"), name="j_0", color="red", render_style="hold")
            
            #plc.padding = 50
            #plc.padding_top = 75
            plc.tools.append(PanTool(plc))
            zoom = ZoomTool(component=plc, tool_mode="box", always_on=False)
            plc.overlays.append(zoom)
            
            # Tweak some of the plot properties
            plc.padding = 50
            #zoom = ZoomTool(component=plot1, tool_mode="box", always_on=False)
            #plot1.overlays.append(zoom)
            
            # Attach some tools to the plot
            #attach_tools(plc)
            plc.bg_color = None
            plc.fill_padding = True
            

    def default_traits_view(self):
        traits_view = View(
            Group(
                Item('plot',
                    editor=ComponentEditor(size=size),
                    show_label=False),
                orientation="vertical"),
            menubar=MenuBar(
                Menu(Action(name="Save Plot", action="save"),
                     Action(name="Load Plot", action="load"),
                     Separator(), CloseAction,
                     name="File")),
            resizable=True,
            title=title,
            handler=ImageFileController)
        return traits_view
    
    '''
    def _plot_default(self):
        
        # Create some x-y data series to plot
        x = linspace(-2.0, 10.0, 400)
        self.pd = pd = ArrayPlotData(index=x, y0=jn(0,x), default_origin="top left")

        # Create some line plots of some of the data
        plot1 = Plot(self.pd,
            title="render_style = hold",
            padding=50, border_visible=True, overlay_border=True)

        plot1.legend.visible = True
        plot1.plot(("index", "y0"), name="j_0", color="red", render_style="hold")
        
        plot1.padding = 50
        plot1.padding_top = 75
        plot1.tools.append(PanTool(plot1))
        #zoom = ZoomTool(component=plot1, tool_mode="box", always_on=False)
        #plot1.overlays.append(zoom)

        # Attach some tools to the plot
        attach_tools(plot1)

        # Create a second scatter plot of one of the datasets, linking its
        # range to the first plot
        plot2 = Plot(self.pd, range2d=plot1.range2d,
            title="render_style = connectedhold",
            padding=50, border_visible=True, overlay_border=True)

        plot2.plot(('index', 'y0'), color="blue", render_style="connectedhold")
        
        plot2.padding = 50
        plot2.padding_top = 75
        plot2.tools.append(PanTool(plot2))
        #zoom = ZoomTool(component=plot2, tool_mode="box", always_on=False)
        #plot2.overlays.append(zoom)
        
        attach_tools(plot2)

        # Create a container and add our plots
        container = HPlotContainer()
        container.add(plot1)
        container.add(plot2)
        return container
    '''
    
    def _save(self):
        win_size = self.plot.outer_bounds
        plot_gc = PlotGraphicsContext(win_size)
        plot_gc.render_component(self.plot)
        plot_gc.save(self._save_file)

    def _load(self):
        try:
            image = ImageData.fromfile(self._load_file)
            self.pd.set_data('imagedata', image._data)
            self.plot.title = "YO DOGG: %s" % os.path.basename(self._load_file)
            self.plot.request_redraw()
        except Exception, exc:
            print "YO DOGG: %s" % exc

class ImageFileController(Handler):
    view = Instance(Demo)
    
    def init(self, info):
        self.view = info.object
    
    def save(self, ui_info):
        ui = self.view.edit_traits(view='save_file_view')
        if ui.result == True:
            self.view._save()
    
    def load(self, ui_info):
        ui = self.view.edit_traits(view='load_file_view')
        if ui.result == True:
            self.view._load()

if __name__ == "__main__":
    demo = Demo()
    demo.configure_traits()

#--EOF---
