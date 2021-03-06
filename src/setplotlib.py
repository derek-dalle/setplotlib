"""
This is a toolkit for modifying matplotlib figures for print quality.

Primarily, it reduces figures to an appropriate size so that fonts will
appear readable when plots are saved to file.

It also has several other functionalities, which will be described here:


"""

# Obviously matplotlib is needed
import matplotlib
# We need array to set the position at the end.
from numpy import array

# Function to configure entire figures
def set_plot(h_f=None):
	"""
	h = set_plot(h_f)
	
	INPUTS:
	  h_f : figure handle, this can be given in several ways:
	    matplotlib.figure.Figure : figure object, as from gcf()
	    matplotlib.axes.Axes     : axes object, will find parent
	    int                      : uses output from figure(h_f)
	        
	
	OUTPUTS:
	  h   : dictionary of various handles from the figure
	
	This function customizes a figure so that it can be saved to file 
	with 3.25 inches width and font at size 9, which is consistent with
	many journals' formatting guidelines.
	"""
	
	# Check the input.
	if h_f == None:
		# Try to get the most recent figure.
		try:
			# Call the GCF function from pyplot
			h_f = matplotlib.pyplot.gcf();
		except:
			# Exit
			raise ValueError("No figures have been drawn.");
	elif isinstance(h_f, int):
		# Figure number given
		h_f = matplotlib.pyplot.figure(h_f);
	elif isinstance(h_f, matplotlib.figure.Figure):
		# This is great; do nothing in this case.
		pass
	elif isinstance(h_f, matplotlib.axes.Axes):
		# Reassign from the parent.
		h_f = h_f.get_figure();
	elif hasattr(h_f, 'get_axes'):
		# Reassign from a parent of a parent.
		h_f = h_f.get_axes().get_figure();
	elif isinstance(h_f, list) and hasattr(h_f[0], 'get_axes'):
		# Reassign from a parent of a parent.
		h_f = h_f[0].get_axes().get_figure();
	else: 
		# Not an acceptable object
		raise ValueError("Input type not recognized.");
	
	# Get the axes.
	h_a = h_f.get_axes();
	# Check for evil subplots.
	if len(h_a) == 0:
		# Empty figure.
		raise ImportError("No axes to manipulate!");
	
	# Now get the size of the figure.
	L_x_i = h_f.get_figwidth()  + 0.0;
	L_y_i = h_f.get_figheight() + 0.0;
	# Calculate the aspect ratio.
	AR_f_i = L_y_i / L_x_i;
	# And the dots per inch.
	dpi_f_i = h_f.get_dpi() + 0.;
	
	# NOTE: This will eventually be set by the input!
	# Desired width of the figure
	L_x = 3.25; # in
	# Desired aspect ratio
	AR_f = AR_f_i;
	# Get the output height
	L_y = L_x * AR_f + 0.0;
	# Determine the correct DPI to keep the same window size.
	dpi_f = L_x_i / L_x * dpi_f_i + 0.0;
	# Apply the size changes to the figure.
	matplotlib.pyplot.setp(h_f, 
		'figwidth' , L_x  ,
		'figheight', L_y  ,
		'dpi'      , dpi_f);
	
	# Find ALL the text objects
	h_t = h_f.findobj(matplotlib.text.Text);
	# Loop through and set the text to good values.
	for h in h_t:
		# Standard font size
		h.set_size(9);
		# Really make it use Times New Roman.
		h.set_family('Times New Roman');
	
	# Loop through all axes.
	for h in h_a:
		# Get handles for the tick marks.
		h_t_x = h.get_xticklines();
		h_t_y = h.get_yticklines();
		# NOTE: This will be controlled by user options.
		# Put the ticks in the correct location
		matplotlib.pyplot.setp(h_t_x, 'marker', 3);
		matplotlib.pyplot.setp(h_t_y, 'marker', 0);
		# Make them smaller (or the right size, anyway).
		matplotlib.pyplot.setp(h_t_x, 'markersize', 2);
		matplotlib.pyplot.setp(h_t_y, 'markersize', 2);
		# Delete the right and top box ("spines").
		h.spines['right'].set_color('none');
		h.spines['top'].set_color('none');
		# Tone done the remaining splines.
		h.spines['left'].set_lw(0.8);
		h.spines['bottom'].set_lw(0.8);
		# Turn off the extra ticks.
		h.xaxis.set_ticks_position('bottom');
		h.yaxis.set_ticks_position('left');
	
	# Final update.
	if matplotlib.pyplot.isinteractive():
		matplotlib.pyplot.draw();
	
	# Ok, let's see if the tight_layout works.
	h_f.tight_layout(pad=0.2);
	
	# Get the top-level line objects.
	h_l = [h.get_lines() for h in h_a];
	# Make a dictionary of the useful handles.
	h = {
		'figure': h_f,
		'axes'  : h_a,
		'lines' : h_l,
		'text'  : h_t};
	# Output
	return h

# Function to make all TEXT labels just fit.
def tight_text(h_f=None):
	"""
	tight_text(h_f)
	
	INPUTS:
	    h_f : figure handle (matplotlib.figure.Figure object)
	
	OUTPUTS:
	    none
	
	This function rescales your axes so that all text objects fit inside
	the print window.  It does not give predictable results if subplots
	are being used.
	"""
	# Check the input.
	if h_f == None:
		# Try to get the most recent figure.
		try:
			# Call the GCF function from pyplot
			h_f = matplotlib.pyplot.gcf();
		except:
			# Exit
			raise ValueError("No figures have been drawn.");
	elif isinstance(h_f, int):
		# Figure number given
		h_f = matplotlib.pyplot.figure(h_f);
	elif isinstance(h_f, matplotlib.figure.Figure):
		# This is great; do nothing in this case.
		pass
	elif isinstance(h_f, matplotlib.axes.Axes):
		# Reassign from the parent.
		h_f = h_f.get_figure();
	elif hasattr(h_f, 'get_axes'):
		# Reassign from a parent of a parent.
		h_f = h_f.get_axes().get_figure();
	elif isinstance(h_f, list) and hasattr(h_f[0], 'get_axes'):
		# Reassign from a parent of a parent.
		h_f = h_f[0].get_axes().get_figure();
	else: 
		# Not an acceptable object
		raise ValueError("Input type not recognized.");
	
	# Get the axes.
	h_a = h_f.get_axes();
	# Check for evil subplots.
	if len(h_a) == 0:
		# Empty figure.
		raise ImportError("No axes to manipulate!");
	# Extract the first axis.
	h_a = h_a[0]
	
	# Set buffers (in inches).
	b_l = 2./72;
	b_r = 2./72;
	b_b = 2./72;
	b_t = 2./72;
	
	# Desired width of the figure
	L_x = h_f.get_figwidth()
	# Get the output height
	L_y = h_f.get_figheight()
	# Determine the correct DPI to keep the same window size.
	dpi_f = h_f.get_dpi()
	# Check for interactive mode.
	if matplotlib.pyplot.isinteractive():
		# Update the text box locations.
		matplotlib.pyplot.draw();
		# Initialize the coordinates for the containing box.
		x_min = L_x*dpi_f+0.0; x_max = 0.0;
		y_min = L_y*dpi_f+0.0; y_max = 0.0;
		# Loop through text objs again to find limits.
		for h in h_f.findobj(matplotlib.text.Text):
			# Ignore empty strings.
			if not (h._renderer is None) and h.get_text():
				# Get the containing box for the object.
				bb = h.get_window_extent();
				# Compare limits to running values.
				x_min = min(x_min, bb.xmin);
				x_max = max(x_max, bb.xmax);
				y_min = min(y_min, bb.ymin);
				y_max = max(y_max, bb.ymax);
		# Bounding box of the existing axes object.
		bb_a_i = h_a.get_position();
		# Calculate the minimum required margins to fit all text.
		margin_l =  bb_a_i.xmin*L_x - x_min/dpi_f;
		margin_r = -bb_a_i.xmax*L_x + x_max/dpi_f;
		margin_b =  bb_a_i.ymin*L_y - y_min/dpi_f;
		margin_t = -bb_a_i.ymax*L_y + y_max/dpi_f;
	else:
		# Not interactive mode... guess the margins.
		margin_l = 0.3;
		margin_r = 0.06;
		margin_b = 0.3;
		margin_t = 0.08;
	
	# Final axis location to contain text and buffers.
	xmin_a = (margin_l + b_l) / L_x;
	ymin_a = (margin_b + b_b) / L_y;
	xmax_a = 1 - (margin_r + b_r) / L_x;
	ymax_a = 1 - (margin_t + b_t) / L_y;
	# Make a bounding box out of these parameters.
	bb_a = matplotlib.transforms.Bbox(
		array([[xmin_a, ymin_a], [xmax_a, ymax_a]]));
	# Apply it!
	h_a.set_position(bb_a);
	# Update
	matplotlib.pyplot.drawifinteractive()

