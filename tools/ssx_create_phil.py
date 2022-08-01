from gladier import GladierBaseTool, generate_flow_definition

def create_phil(**data):
    """Create a phil file for dials-stills if one doesn't already exist
    The Phil file uses a template set directly on the script and can be updated according to new options on dials
    - data['data_dir'] is the path where the raw (cbf) data is stored
    - data['proc_dir'] is the path to where dials will run and save results
    Optional variables can be passed to overwrite the default values
    - data['unit_cell']
    - data['beamx']
    - data['beamy']
    - data['nproc']
    - data['mask']
    If a file xy.json exists in the data_dir it will override beamx and beamy variables
    """
    import json
    import os
    from string import Template

    data_dir = data['data_dir']
        
    phil_name = f"{data_dir}/process.phil"

    if os.path.isfile(phil_name):
        return phil_name
    
    ##Getting optional variables
    unit_cell = data.get('unit_cell', None)
    beamx = data.get('beamx', -214.400)
    beamy = data.get('beamy', 218.200)
    nproc = data.get('nproc', 32)
    mask_file = data.get('mask', 'mask.pickle')

    ##opening existing files
    beamline_json = os.path.join(data_dir,f"beamline_run.json")
    mask = os.path.join(data_dir,mask_file)

    beamline_data = None

    try:
        with open(beamline_json, 'r') as fp:
            beamline_data = json.loads(fp.read())

        if not unit_cell:
            unit_cell = beamline_data['user_input']['unit_cell']

        unit_cell = unit_cell.replace(",", " ")
        space_group = beamline_data['user_input']['space_group']
        det_distance = float(beamline_data['beamline_input']['det_distance']) * -1.0
    except:
        pass

    template_data = {'det_distance': det_distance,
                     'unit_cell': unit_cell,
                     'nproc': nproc,
                     'space_group': space_group,
                     'beamx': beamx,
                     'beamy': beamy,
                     'mask': mask}

    template_phil = Template("""spotfinder.lookup.mask=$mask
integration.lookup.mask=$mask
spotfinder.filter.min_spot_size=2
significance_filter.enable=True
#significance_filter.isigi_cutoff=1.0
mp.nproc = $nproc
mp.method=multiprocessing
output.composite_output=False
refinement.parameterisation.detector.fix=none
geometry {
  detector {
      panel {
                fast_axis = 0.9999673162585729, -0.0034449798523932267, -0.007314268824966957
                slow_axis = -0.0034447744696749034, -0.99999406591948, 4.0677756813531234e-05
                origin    = $beamx, $beamy, $det_distance
                }
            }
         }
indexing {
  known_symmetry {
    space_group = $space_group
    unit_cell = $unit_cell
  }
  stills.indexer=stills
  stills.method_list=fft1d
  multiple_lattice_search.max_lattices=3
}""")
    phil_data = template_phil.substitute(template_data)

    with open(phil_name, 'w') as fp:
        fp.write(phil_data)
    return phil_name 

@generate_flow_definition(modifiers={
    'create_phil': {'endpoint': 'funcx_endpoint_non_compute',
                           'ExceptionOnActionFailure': True,
                           }
})
class CreatePhil(GladierBaseTool):
    flow_input = {}
    required_input = [
        'data_dir',
        'funcx_endpoint_non_compute',
    ]
    funcx_functions = [create_phil]
