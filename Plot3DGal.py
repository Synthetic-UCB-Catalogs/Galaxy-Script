#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:05:24 2024

@author: alexey
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import pyvista as pv
import os
import legwork.source as source
import legwork.visualisation as vis
import astropy.units as u
import seaborn as sns
from matplotlib.colors import TwoSlopeNorm
import matplotlib.cm as mcm  # Import matplotlib's cm module as mcm to avoid confusion
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
import cmasher as cmr

sys.path.insert(1, './PyModules/')


Make3DMap      = False
MakeGalView    = False
LEGWORKStepQ   = False
AnimationStepQ = True

# Read in the Galaxy data
df  = pd.read_csv('./FullGalaxyDWDLISAOnly.csv')
# Extracting the columns
x   = df['Xkpc']
y   = df['Ykpc']
z   = df['Zkpc']



if Make3DMap:
    # Create a new figure for the 3D plot with high DPI
    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(111, projection='3d', facecolor='black')

    # Plotting the points
    ax.scatter(x, y, z, color='lime', s=3, alpha=0.02)  # 's' is the size of the points

    # Set the background color
    ax.set_facecolor('black')

    AxRange = 15

    # Set the range for all axes
    ax.set_xlim([-AxRange, AxRange])
    ax.set_ylim([-AxRange, AxRange])
    ax.set_zlim([-AxRange, AxRange])

    # Set the labels and title with colors
    ax.set_xlabel('X, kpc', color='white')
    ax.set_ylabel('Y, kpc', color='white')
    ax.set_zlabel('Z, kpc', color='white')

    # Change the color of the tick labels to white
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.tick_params(axis='z', colors='white')

    # Save the plot as a high-resolution image
    plt.savefig('./LISAGalTestFullMany.png', dpi=300, bbox_inches='tight', pad_inches=0.1, facecolor='black')

if MakeGalView:
    print(df.columns)
    #Pre-setup plot options, suited for an 8cm MNRAS single-column figure
    cm  = 1/2.54  # centimeters in inches
    DPI = 300
    LW  = 3       
    plt.clf()
    #plt.rc('font', family='fantasy', size=11)
    #plt.rc('font', family='')
    #plt.rcParams["font.family"] = "fantasy"
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams['mathtext.fontset'] = 'cm'
    sns.set_style("white")
    sns.set_context("paper")
    


    fig = plt.figure(figsize=(14*cm,7*cm), constrained_layout=True)
    
    ax = plt.gca()    
    scatter = ax.scatter(df["Gall"]*(180/(np.pi)),df["Galb"]*(180/(np.pi)),c=df['Age'],s=1, cmap='cmr.cosmic')
        
           
    #ax.set_xscale('log')
    #ax.set_yscale('log')
    plt.xlim([0, 360])  
    plt.ylim([-90, 90])  

    
    plt.xlabel(r'l, deg')
    plt.ylabel(r'b, deg')
    #plt.legend(loc="right", fontsize=7)
    #fig.colorbar(cm.ScalarMappable(cmap='cmr.cosmic'), ax=ax)
    #fig.colorbar(mcm.ScalarMappable(cmap='cmr.cosmic'), ax=ax)
    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label('Age (Gyr)', rotation=270, labelpad=10)
    
    plt.savefig('./GalaxyCoordsAgeDWDLISAOnly.png', dpi=DPI)   

    df['FeH'][df['FeH'] >0.4] = 0.4

    fig = plt.figure(figsize=(14*cm,7*cm), constrained_layout=True)
    
    ax = plt.gca()    
    scatter = ax.scatter(df["Gall"]*(180/(np.pi)),df["Galb"]*(180/(np.pi)),c=df['FeH'],s=1, cmap='cmr.cosmic')
                   
    #ax.set_xscale('log')
    #ax.set_yscale('log')
    plt.xlim([0, 360])  
    plt.ylim([-90, 90])  

    
    plt.xlabel(r'l, deg')
    plt.ylabel(r'b, deg')
    #plt.legend(loc="right", fontsize=7)
    #fig.colorbar(cm.ScalarMappable(cmap='cmr.cosmic'), ax=ax)
    #fig.colorbar(mcm.ScalarMappable(cmap='cmr.cosmic'), ax=ax)
    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label('[Fe/H]', rotation=270, labelpad=10)
    
    plt.savefig('./GalaxyCoordsFeHDWDLISAOnly.png', dpi=DPI)
    
    cm_to_inch = 1 / 2.54
    nrows=4
    ncols=3
    bin_values = sorted(df['Bin'].unique())
    n_bins = len(bin_values)
    
    fig, axes = plt.subplots(
    nrows,
    ncols,
    figsize=(14 * cm_to_inch * ncols, 7 * cm_to_inch * nrows),
    constrained_layout=True)

    axes = axes.flatten()
    
    vmin = df['FeH'].min()
    vmax = df['FeH'].max()
    
    Labels = np.array(['Thin Disk 1', 'Thin Disk 2','Thin Disk 3','Thin Disk 4','Thin Disk 5','Thin Disk 6','Thin Disk 7','Thick Disk','Halo','Bulge'])
    for i, (bin_value, ax) in enumerate(zip(bin_values, axes)):
        # Filter DataFrame for the current 'Bin' value
        df_bin = df[df['Bin'] == bin_value]
    
        # Create scatter plot
        scatter = ax.scatter(
            df_bin["Gall"] * (180 / np.pi),
            df_bin["Galb"] * (180 / np.pi),
            c=df_bin['FeH'],
            s=1,
            cmap='cmr.cosmic',
            vmin=vmin,
            vmax=vmax
        )

        # Set axis limits and labels
        ax.set_xlim([0, 360])
        ax.set_ylim([-90, 90])
        ax.set_xlabel('l, deg')
        ax.set_ylabel('b, deg')
        ax.set_title(Labels[i])
                   
    #ax.set_xscale('log')
    #ax.set_yscale('log')
    plt.xlim([0, 360])  
    plt.ylim([-90, 90])  

    # Remove any unused subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    # Create a ScalarMappable for the colorbar
    norm = Normalize(vmin=vmin, vmax=vmax)
    cmap = cmr.cosmic
    sm = ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])  # Required for ScalarMappable

    # Add the colorbar to the figure
    cbar = fig.colorbar(
        sm,
        ax=axes.ravel().tolist(),
        orientation='vertical',
        fraction=0.02,
        pad=0.04
    )
    cbar.set_label('[Fe/H]', rotation=270, labelpad=15)
    
    plt.savefig('./GalaxyCoordsFeHBinnedDWDLISAOnly.png', dpi=DPI)
    


#LEGWORK part
if LEGWORKStepQ:

    n_values = len(df.index)

    m_1    = (df['mass1']).to_numpy() * u.Msun
    m_2    = (df['mass2']).to_numpy() * u.Msun
    dist   = (df['RRelkpc']).to_numpy() * u.kpc
    f_orb = (1/(df['PSetTodayHours']*60*60)).to_numpy() * u.Hz
    ecc   = np.zeros(n_values)
    
    sources = source.Source(m_1=m_1, m_2=m_2, ecc=ecc, dist=dist, f_orb=f_orb)
    snr     = sources.get_snr(verbose=True)
    
    cutoff = 7
    
    detectable_threshold = cutoff
    detectable_sources   = sources.snr > cutoff
    print("{} of the {} sources are detectable".format(len(sources.snr[detectable_sources]), n_values))
    
    # create the same plot but set `show=False`
    fig, ax = sources.plot_source_variables(xstr="f_orb", ystr="snr", disttype="kde", log_scale=(True, True),
                                            fill=True, show=False, which_sources=sources.snr > 7, figsize=(10, 8))
    
    #ax.set_aspect(0.8)
    
    # duplicate the x axis and plot the LISA sensitivity curve
    right_ax = ax.twinx()
    frequency_range = np.logspace(np.log10(2e-6), np.log10(2e-1), 1000) * u.Hz
    vis.plot_sensitivity_curve(frequency_range=frequency_range, fig=fig, ax=right_ax,fill=False)
    
    # Adjust layout to prevent cropping
    fig.tight_layout()
    
    fig.savefig('./SensitivityCurveLISAOnly.png', bbox_inches='tight')

if AnimationStepQ:
    
    # Ensure the output directory exists
    output_dir = './Frames/'
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Load the galaxy data
    data = df
    
    # Extract X, Y, Z coordinates
    points = data[['Xkpc', 'Ykpc', 'Zkpc']].values
    
    # Create a PyVista point cloud
    point_cloud = pv.PolyData(points)
    
    # Initialize the plotter
    plotter = pv.Plotter(off_screen=True, window_size=(800, 600))
    plotter.set_background('black')
    
    # Add the point cloud to the plotter with styling
    plotter.add_mesh(
        point_cloud,
        color='white',
        point_size=0.5,
        render_points_as_spheres=True,
        opacity=0.8,
        )
    
    # Camera and animation settings
    num_frames = 360  # Total number of frames
    fps = 30  # Frames per second
    radius = np.max(np.linalg.norm(points[:, :2], axis=1)) * 1.2  # Orbit radius
    elevation_angle = np.radians(30)  # Elevation angle above the galactic plane
    angles = np.linspace(0, 4 * np.pi, num_frames)  # Two full orbits
    
    # Generate and save each frame
    for i, angle in enumerate(angles):
        # Calculate camera position
        x = radius * np.cos(angle) * np.cos(elevation_angle)
        y = radius * np.sin(angle) * np.cos(elevation_angle)
        z = radius * np.sin(elevation_angle)
        
        # Update camera settings
        plotter.camera_position = [
            (x, y, z),  # Camera position
            (0, 0, 0),  # Look at the galactic center
            (0, 0, 1),  # Up direction
            ]
        plotter.camera.view_angle = 60  # Human eye field of view
        
        
        # Render and save the frame
        filename = os.path.join(output_dir, f'frame_{i:04d}.png')
        plotter.show(screenshot=filename, auto_close=False)
        plotter.clear()  # Clear the plotter for the next frame
        sys.exit()
    # Close the plotter after rendering
    plotter.close()
