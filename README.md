# Blender Bezier Curve Exporter
============

Exports Splines from Blender to Megashapes plugin for Unity

## Installation

Copy the io_scene_sxl to the scripts/addons folder. 

## Usage

Activate addon from "User Preferences > Addons" and use Export from menu (Export -> Bezier Curve (*.sxl) ).

Due to Megashapes limitation only one spline should be selected. Normal import doesn't create new line objects to 
Unity. Exporter supports still exporting everything but default is Selected Only.

Tilt is not supported in current version on Megashapes.

Default Forward and Up settings work for Unity (Forward > Z Forward and Up > Y Up)

Scale can be used to scale spline to Unity.


