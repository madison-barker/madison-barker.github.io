import gpxpy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cartopy.crs as ccrs
from cartopy.io.img_tiles import OSM
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

"""

This code will read in a .gpx file (such as one downloaded from Ride With GPS), create an image of the geocoordinates provided in the gpx file, and output an animation that will show the planned route.

Created by Madison Barker on 2/1/24

"""

# parse GPX file from Ride With GPS
def parse_gpx(file_path):
    gpx_file = open(file_path, 'r')
    gpx = gpxpy.parse(gpx_file)
    return gpx.tracks[0].segments[0].points

# generate image of map using Cartopy and OSM
def create_map_image():
    fig = plt.figure(figsize=(10, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree())
    ax.add_image(OSM(), 10)
    return fig, ax
    
# animate data and export as .mp4
def animate_route(gpx_data, output_file, fps=30):
    fig, ax = create_map_image()
    latitudes = [point.latitude for point in gpx_data]
    longitudes = [point.longitude for point in gpx_data]

    line, = ax.plot([], [], '-o', markersize=2, color='red', transform=ccrs.PlateCarree())
    ax.set_xlim(min(longitudes), max(longitudes))
    ax.set_ylim(min(latitudes), max(latitudes))

    def animate(i):
        x = longitudes[:i]
        y = latitudes[:i]
        line.set_data(x, y)
        return line,

    ani = animation.FuncAnimation(fig, animate, frames=len(gpx_data), repeat=False, interval=1000 / fps)
    ani.save(output_file, writer='ffmpeg', dpi=100, fps=fps) # adjust as needed

if __name__ == "__main__":
    gpx_file_path = "Name_Of_Your_File.gpx"
    output_video_file = "Any_Name_Your_Heart_Desires.mp4"
    fps = 60  # Adjust the frames per second as needed

    gpx_data = parse_gpx(gpx_file_path)
    animate_route(gpx_data, output_video_file, fps)

    plt.show()
