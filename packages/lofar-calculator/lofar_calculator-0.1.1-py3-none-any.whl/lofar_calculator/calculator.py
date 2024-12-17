"""Main file for LUCI"""

__author__ = "Sarrvesh S. Sridhar"
__email__ = "sarrvesh@astron.nl"

from random import randint
import os
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import flask
from lofar_calculator.gui import layout
import lofar_calculator.backend as bk
import lofar_calculator.targetvis as tv
import lofar_calculator.generatepdf as g

# Initialize the dash app
server = flask.Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN], \
                server=server, url_base_pathname='/luci/')
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

#######################################
# Setup the layout of the web interface
#######################################
app.layout = layout
app.title = 'LUCI - LOFAR Unified Calculator for Imaging'

##############################################
# TODO: Move all callbacks to a separate file
# See https://community.plot.ly/t/dash-callback-in-a-separate-file/14122/16
##############################################

##############################################
# Show pipeline fields based on dropdown value
##############################################
@app.callback(
    [Output('tAvgRowL', 'style'),
     Output('tAvgRow', 'style'),
     Output('fAvgRowL', 'style'),
     Output('fAvgRow', 'style'),
     Output('dyCompressRowL', 'style'),
     Output('dyCompressRow', 'style'),
     Output('pipeSizeRowL', 'style'),
     Output('pipeSizeRow', 'style'),
     Output('pipeProcTimeRow', 'style'),
     Output('pipeProcTimeRowL', 'style')
    ],
    [Input('pipeTypeRow', 'value')]
)
def toggle_pipeline(value):
    """Function to show relevant pipeline fields depending on
       the user's pipeline choice."""
    if value == 'none':
        return {'display':'none'}, {'display':'none'}, \
               {'display':'none'}, {'display':'none'}, \
               {'display':'none'}, {'display':'none'}, \
               {'display':'none'}, {'display':'none'}, \
               {'display':'none'}, {'display':'none'}
    elif value == 'preprocessing':
        return {'display':'block'}, {'display':'block'}, \
               {'display':'block'}, {'display':'block'}, \
               {'display':'block'}, {'display':'block'}, \
               {'display':'block'}, {'display':'block'}, \
               {'display':'block'}, {'display':'block'}

#######################################
# Validate time averaging factor
#######################################
@app.callback(
    Output('msgboxTAvg', 'is_open'),
    [Input('tAvgRow', 'n_blur'),
     Input('mbtAvgClose', 'n_clicks')
    ],
    [State('tAvgRow', 'value'),
     State('msgboxTAvg', 'is_open')
    ]
)
def validate_t_avg(n_blur, n_clicks, value, is_open):
    """Validate time averaging factor and display error message if needed"""
    if is_open is True and n_clicks is not None:
        # The message box is open and the user has clicked the close
        # button. Close the alert message
        return False
    if n_blur is None:
        # The page is loading. Do not validate anything
        return False
    else:
        # Text box has lost focus.
        # Go ahead and validate the text in it.
        try:
            int(str(value))
        except ValueError:
            return True
        return False

#######################################
# Validate freq averaging factor
#######################################
@app.callback(
    Output('msgboxFAvg', 'is_open'),
    [Input('fAvgRow', 'n_blur'),
     Input('mbfAvgClose', 'n_clicks')
    ],
    [State('fAvgRow', 'value'),
     State('msgboxFAvg', 'is_open')
    ]
)
def validate_t_avg(n_blur, n_clicks, value, is_open):
    """Validate frequency averaging factor and display error message if needed"""
    if is_open is True and n_clicks is not None:
        # The message box is open and the user has clicked the close
        # button. Close the alert message
        return False
    if n_blur is None:
        # The page is loading. Do not validate anything
        return False
    else:
        # Text box has lost focus.
        # Go ahead and validate the text in it.
        try:
            int(str(value))
        except ValueError:
            return True
        return False

#######################################
# What should the resolve button do?
#######################################
@app.callback(
    [Output('coordRow', 'value'),
     Output('msgboxResolve', 'is_open')
    ],
    [Input('resolve', 'n_clicks'),
     Input('mbResolveClose', 'n_clicks')
    ],
    [State('targetNameRow', 'value'),
     State('msgboxResolve', 'is_open')
    ]
)
def on_resolve_click(n, close_msg_box, target_name, is_open):
    """Function defines what to do when the resolve button is clicked"""
    if is_open is True and close_msg_box is not None:
        # The message box is open and the user has clicked the close
        # button. Close the alert message
        return '', False
    if n is None:
        # The page has just loaded.
        return '', False
    else:
        # Resole button has been clicked
        coord_str = tv.resolve_source(target_name)
        if coord_str is None:
            # Display error message.
            return '', True
        else:
            return coord_str, False

#######################################
# What should the export button do?
#######################################
@app.callback(
    [Output('download-link', 'style'),
     Output('download-link', 'href'),
     Output('msgboxGenPdf', 'is_open')
    ],
    [Input('genpdf', 'n_clicks'),
     Input('mbGenPdfClose', 'n_clicks')
    ],
    [State('obsTimeRow', 'value'),
     State('nCoreRow', 'value'),
     State('nRemoteRow', 'value'),
     State('nIntRow', 'value'),
     State('nChanRow', 'value'),
     State('nSbRow', 'value'),
     State('intTimeRow', 'value'),
     State('hbaDualRow', 'value'),
     State('coordRow', 'value'),

     State('pipeTypeRow', 'value'),
     State('tAvgRow', 'value'),
     State('fAvgRow', 'value'),
     State('dyCompressRow', 'value'),

     State('rawSizeRow', 'value'),
     State('pipeSizeRow', 'value'),
     State('pipeProcTimeRow', 'value'),
     State('sensitivity-table', 'figure'),

     State('msgboxGenPdf', 'is_open'),

     State('elevation-plot', 'figure'),
     State('distance-table', 'figure'),

     State('dateRow', 'date')
    ]
)
def on_genpdf_click(n_clicks, close_msg_box, obs_t, n_core, n_remote, n_int, n_chan,
                    n_sb, integ_t, ant_set, coord, pipe_type, t_avg, f_avg, is_dysco,
                     raw_size, proc_size, pipe_time, sensitivity_table, is_msg_box_open,
                    elevation_fig_pdf, distance_table, obs_date):
    """Function defines what to do when the generate pdf button is clicked"""
    if is_msg_box_open is True and close_msg_box is not None:
        # The message box is open and the user has clicked the close
        # button. Close the alert message.
        return {'display':'none'}, '', False
    if n_clicks is None:
        # Generate button has not been clicked. Hide the download link
        return {'display':'none'}, '', False
    else:
        if raw_size is '':
            # User has clicked generate PDF button before calculate
            return {'display':'none'}, '', True
        else:
            # Generate a random number so that this user's pdf can be stored here
            randnum = '{:05d}'.format(randint(0, 10000))
            rel_path = 'static/'
            # Generate a relative and absolute filenames to the pdf file
            rel_path = os.path.join(rel_path, 'summary_{}.pdf'.format(randnum))
            abs_path = os.path.join(os.getcwd(), rel_path)
            g.generate_pdf(rel_path, obs_t, n_core, n_remote, n_int, n_chan,
                           n_sb, integ_t, ant_set, pipe_type, t_avg, f_avg,
                           is_dysco, raw_size, proc_size, pipe_time, sensitivity_table,
                           elevation_fig_pdf, distance_table, obs_date)
            return {'display':'block'}, '/luci/{}'.format(rel_path), False

@app.server.route('/luci/static/<resource>')
def serve_static(resource):
    path = os.path.join(os.getcwd(), 'static')
    return flask.send_from_directory(path, resource)

#######################################
# What should the submit button do?
#######################################
@app.callback(
    [Output('rawSizeRow', 'value'),
     Output('pipeSizeRow', 'value'),
     Output('pipeProcTimeRow', 'value'),
     Output('sensitivity-table', 'style'),
     Output('sensitivity-table', 'figure'),
     Output('msgBoxBody', 'children'),
     Output('msgbox', 'is_open'),
     Output('alert_box', 'is_open'),
     Output('elevation-plot', 'style'),
     Output('elevation-plot', 'figure'),
     Output('beam-plot', 'style'),
     Output('beam-plot', 'figure'),
     Output('distance-table', 'style'),
     Output('distance-table', 'figure')
    ],
    [Input('calculate', 'n_clicks'),
     Input('msgBoxClose', 'n_clicks'),
    ],
    [State('obsTimeRow', 'value'),
     State('nCoreRow', 'value'),
     State('nRemoteRow', 'value'),
     State('nIntRow', 'value'),
     State('nChanRow', 'value'),
     State('nSbRow', 'value'),
     State('intTimeRow', 'value'),
     State('hbaDualRow', 'value'),
     State('pipeTypeRow', 'value'),
     State('tAvgRow', 'value'),
     State('fAvgRow', 'value'),
     State('dyCompressRow', 'value'),
     State('msgbox', 'is_open'),
     State('alert_box', 'is_open'),
     State('targetNameRow', 'value'),
     State('coordRow', 'value'),
     State('dateRow', 'date'),
     State('calListRow', 'value'),
     State('demixListRow', 'value')
    ]
)
def on_calculate_click(n, n_clicks, obs_t, n_core, n_remote, n_int, n_chan, n_sb,
                       integ_t, hba_mode, pipe_type, t_avg, f_avg, dy_compress,
                       is_open, is_open_2, src_name, coord, obs_date, calib_names,
                       ateam_names):
    """Function defines what to do when the calculate button is clicked"""
    if is_open is True:
        # User has closed the error message box
        return '', '', '', {'display':'none'}, {}, '', False, False,\
               {'display':'none'}, {}, {'display':'none'}, \
               {}, {'display':'none'}, {}
    if n is None:
        # Calculate button has not been clicked yet
        # So, do nothing and set default values to results field
        return '', '', '', {'display':'none'}, {}, '', False, False,\
               {'display':'none'}, {}, {'display':'none'}, {}, \
               {'display':'none'}, {}
    else:
        # Calculate button has been clicked.
        # First, validate all command line inputs

        # If the user sets n_core, n_remote, or n_int to 0, dash return None.
        # Why is this?
        # Correct this manually, for now.
        if n_core is None:
            n_core = '0'
        if n_remote is None:
            n_remote = '0'
        if n_int is None:
            n_int = '0'
        status, msg = bk.validate_inputs(obs_t, int(n_core), int(n_remote), \
                                         int(n_int), n_sb, integ_t, t_avg, f_avg, \
                                         src_name, coord, hba_mode, pipe_type, \
                                         ateam_names, obs_date)
        if status is False:
            return '', '', '', {'display':'none'}, {}, msg, True, False,\
                   {'display':'none'}, {}, {'display':'none'}, {}, \
                   {'display':'none'}, {}
        else:
            # Estimate the raw data size

            n_baselines = bk.compute_baselines(int(n_core), int(n_remote),
                                               int(n_int), hba_mode)
            im_noise = bk.calculate_im_noise(int(n_core), int(n_remote),
                                             int(n_int), hba_mode, float(obs_t),
                                             int(n_sb))
            raw_size = bk.calculate_raw_size(float(obs_t), float(integ_t),
                                             n_baselines, int(n_chan), int(n_sb))
            avg_size = bk.calculate_proc_size(float(obs_t), float(integ_t),
                                              n_baselines, int(n_chan), int(n_sb),
                                              pipe_type, int(t_avg), int(f_avg),
                                              dy_compress)
            if pipe_type == 'none':
                # No pipeline
                pipe_time = None
            else:
                pipe_time = bk.calculate_pipe_time(float(obs_t), int(n_sb),
                                                   hba_mode, ateam_names,
                                                   pipe_type)

            # It is useful to have coord as a list from now on
            if coord is not '':
                coord_list = coord.split(',')
                coord_input_list = coord.split(',')

            # Add calibrator names to the target list so that they can be
            # plotted together. Before doing that, make a copy of the input
            # target list and its coordinates
            src_name_input = src_name
            coord_input = coord
            if calib_names is not None:
                for i in range(len(calib_names)):
                    if i == 0 and src_name is None:
                        src_name = '{}'.format(calib_names[i])
                        coord_list = [tv.CALIB_COORDINATES[calib_names[i]]]
                    else:
                        src_name += ', {}'.format(calib_names[i])
                        coord_list.append(tv.CALIB_COORDINATES[calib_names[i]])

            # Add A-team names to the target list so that they can be
            # plotted together
            if ateam_names is not None:
                for i in range(len(ateam_names)):
                    if i == 0 and src_name is None:
                        src_name = '{}'.format(ateam_names[i])
                        coord_list = [tv.ATEAM_COORDINATES[ateam_names[i]]]
                    else:
                        src_name += ', {}'.format(ateam_names[i])
                        coord_list.append(tv.ATEAM_COORDINATES[ateam_names[i]])

            if coord is '':
                # No source is specified under Target setup
                display_fig = {'display':'none'}
                elevation_fig = {}
                beam_fig = {}
                display_tab = {'display':'none'}
                distance_tab = {}
                display_sens_tab = {'display':'none'}
                sensitivity_tab = {}
            else:
                # User has specified a coordinate and it has passed validation
                # in the validate_inputs function.
                # Check if the number of SAPs is less than 488
                n_point = len(coord_input_list)
                n_sap = n_point * int(n_sb)
                max_sap = 488
                if n_sap > max_sap:
                    msg = 'Number of targets times number of subbands cannot ' + \
                          'be greater than {}.'.format(max_sap)
                    return '', '', '', {'display':'none'}, {}, msg, True, False,\
                           {'display':'none'}, {}, {'display':'none'}, {}, \
                           {'display':'none'}, {}

                # Create a figure with the elevation of the targets
                elevation_fig = tv.create_fig_add_lst_axis(src_name, coord_list, obs_date, int(n_int), obs_t)


                display_fig = {'display':'block', 'height':600}

                # Find the position of the station and tile beam
                beam_fig = tv.find_beam_layout(src_name_input, coord_input, \
                                   int(n_core), int(n_remote), int(n_int), hba_mode)
                # Calculate distance between all the targets and offending sources
                display_tab = {'display':'block'}
                table_data = [tv.make_distance_table(src_name_input,
                                                     coord_input, obs_date)]
                table_title = 'Angular distances in degrees between specified ' +\
                             'targets and other bright sources'
                distance_tab = {'data':table_data,
                                'layout':{'title':table_title, 'autosize':True}
                               }
                display_sens_tab = {'display':'block', 'height':300}
                sens_table_data = [tv.make_sens_table(src_name_input, coord_input, obs_date, obs_t, n_int, im_noise, hba_mode)]
                sens_table_title = '<b>Sensitivity Results</b>'
                sensitivity_tab = {'data':sens_table_data,
                                'layout':{'title':sens_table_title, 'autosize':True}
                              }

            src_name_list = src_name_list = src_name.split(',')
            maxelev = tv.target_max_elevation(src_name_list, coord, obs_date, n_int)
            if all(i>30 for i in maxelev) == False and 'hba' in hba_mode:
                return raw_size, avg_size, pipe_time, display_sens_tab, sensitivity_tab, '', \
                   False, True, display_fig, elevation_fig, display_fig, beam_fig, \
                   display_tab, distance_tab

            if all(i>40 for i in maxelev) == False and 'lba' in hba_mode:
                return raw_size, avg_size, pipe_time, display_sens_tab, sensitivity_tab, '', \
                   False, True, display_fig, elevation_fig, display_fig, beam_fig, \
                   display_tab, distance_tab

            else:
                return raw_size, avg_size, pipe_time, display_sens_tab, sensitivity_tab, '', \
                   False, False, display_fig, elevation_fig, display_fig, beam_fig, \
                   display_tab, distance_tab

if __name__ == '__main__':
    #app.run_server(debug=True, host='0.0.0.0', port=8051)
    app.run_server(debug=False, host='0.0.0.0', port=8051, \
                  dev_tools_ui=False, dev_tools_props_check=False)
