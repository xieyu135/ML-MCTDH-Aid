
import json
from gener_inp import generInp
from gener_op import generOp
from gener_op_LVC import generOp as generOpLvc

def main(path='config.json'):
    config = json.load(open(path, 'r'))
    generInp(inp_name=config["inp_name"],
            op_name=config["op_name"],
            tfinal=config["tfinal"],
            tout=config["tout"],
            nstate=config["nstate"],
            nmode=config["nmode"],
            )
    if ('model_type' not in config) or (config['model_type']=='spin_boson'):
        generOp(op_type=config["op_type"],
                n_triple=config["n_triple"],
                op_name=config["op_name"],
                fnm_kappa=config["fnm_kappa"],
                fnm_omega=config["fnm_omega"],
                fnm_vmat=config["fnm_vmat"],
                )
    elif config['model_type']=='lvc':
        generOpLvc(op_type=config["op_type"],
                n_triple=config["n_triple"],
                op_name=config["op_name"],
                fnm_kappa=config["fnm_kappa"],
                fnm_omega=config["fnm_omega"],
                fnm_vmat=config["fnm_vmat"],
                fnm_lambda=config["fnm_lambda"],
                )
    else:
        print(f'The model does not exist: {config["model_type"]}')
if __name__=='__main__':
    main(path='config.json')
