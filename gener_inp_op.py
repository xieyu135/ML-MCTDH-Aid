
import json
from gener_inp import generInp
from gener_op import generOp

def main(path='config.json'):
    config = json.load(open(path, 'r'))
    generInp(inp_name=config["inp_name"],
            op_name=config["op_name"],
            tfinal=config["tfinal"],
            tout=config["tout"],
            nstate=config["nstate"],
            nmode=config["nmode"],
            )
    generOp(op_type=config["op_type"],
            n_triple=config["n_triple"],
            op_name=config["op_name"],
            fnm_kappa=config["fnm_kappa"],
            fnm_omega=config["fnm_omega"],
            fnm_vmat=config["fnm_vmat"],
            )
if __name__=='__main__':
    main(path='config.json')