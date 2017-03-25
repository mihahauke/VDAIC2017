from __future__ import print_function
import numpy as np
import sys
sys.path.append('./bin/python')
import vizdoom 
from agent.doom_simulator import DoomSimulator
from agent.agent import Agent
import tensorflow as tf

def main():
    
    ## Simulator
    simulator_args = {}
    simulator_args['config'] = 'config/config.cfg'
    simulator_args['resolution'] = (160,120)
    simulator_args['frame_skip'] = 2
    simulator_args['color_mode'] = 'GRAY'   
    simulator_args['game_args'] = "+name IntelAct +colorset 7"
        
    ## Agent    
    agent_args = {}
    
    # preprocessing
    agent_args['preprocess_input_images'] = lambda x: x / 255. - 0.5
    agent_args['preprocess_input_measurements'] = lambda x: x / 100. - 0.5
    agent_args['num_future_steps'] = 6
    pred_scale_coeffs = np.expand_dims((np.expand_dims(np.array([8.,40.,1.]),1) * np.ones((1,agent_args['num_future_steps']))).flatten(),0)
    agent_args['postprocess_predictions'] = lambda x: x * pred_scale_coeffs
    agent_args['discrete_controls_manual'] = range(6,12) 
    agent_args['meas_for_net_init'] = range(3)
    agent_args['meas_for_manual_init'] = range(3,16)
    agent_args['opposite_button_pairs'] = [(0,1),(2,3)]
    
    # net parameters
    agent_args['conv_params']     = np.array([(16,5,4), (32,3,2), (64,3,2), (128,3,2)],
                                     dtype = [('out_channels',int), ('kernel',int), ('stride',int)])
    agent_args['fc_img_params']   = np.array([(128,)], dtype = [('out_dims',int)])
    agent_args['fc_meas_params']  = np.array([(128,), (128,), (128,)], dtype = [('out_dims',int)]) 
    agent_args['fc_joint_params'] = np.array([(256,), (256,), (-1,)], dtype = [('out_dims',int)])   
    agent_args['target_dim'] = agent_args['num_future_steps'] * len(agent_args['meas_for_net_init'])
    
    # experiment arguments
    agent_args['test_objective_params'] = (np.array([5,11,17]), np.array([1.,1.,1.]))
    agent_args['history_length'] = 1
    agent_args['test_checkpoint'] = 'model'
    
    print('starting simulator')

    simulator = DoomSimulator(simulator_args)
    
    print('started simulator')

    agent_args['discrete_controls'] = simulator.discrete_controls
    agent_args['continuous_controls'] = simulator.continuous_controls
    agent_args['state_imgs_shape'] = (agent_args['history_length']*simulator.num_channels, simulator.resolution[1], simulator.resolution[0])
    if 'meas_for_net_init' in agent_args:
        agent_args['meas_for_net'] = []
        for ns in range(agent_args['history_length']):
            agent_args['meas_for_net'] += [i + simulator.num_meas * ns for i in agent_args['meas_for_net_init']]
        agent_args['meas_for_net'] = np.array(agent_args['meas_for_net'])
    else:
        agent_args['meas_for_net'] = np.arange(agent_args['history_length']*simulator.num_meas)
    if len(agent_args['meas_for_manual_init']) > 0:
        agent_args['meas_for_manual'] = np.array([i + simulator.num_meas*(agent_args['history_length']-1) for i in agent_args['meas_for_manual_init']]) # current timestep is the last in the stack
    else:
        agent_args['meas_for_manual'] = []
    agent_args['state_meas_shape'] = (len(agent_args['meas_for_net']),)
    
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.1)
    sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options,log_device_placement=False))
    ag = Agent(sess, agent_args)
    ag.load('./checkpoints')
    
    img_buffer = np.zeros((agent_args['history_length'], simulator.num_channels, simulator.resolution[1], simulator.resolution[0]))
    meas_buffer = np.zeros((agent_args['history_length'], simulator.num_meas))
    curr_step = 0
    term = False
    
    acts_to_replace = [a+b+d+e for a in [[0,0],[1,1]] for b in [[0,0],[1,1]] for d in [[0]] for e in [[0],[1]]]
    print(acts_to_replace)
    replacement_act = [0,1,0,0,0,1,0,0,0,0,0,0]
    #MOVE_FORWARD   MOVE_BACKWARD   TURN_LEFT   TURN_RIGHT  ATTACK  SPEED   SELECT_WEAPON2  SELECT_WEAPON3  SELECT_WEAPON4  SELECT_WEAPON5  SELECT_WEAPON6  SELECT_WEAPON7

    while not term:
        if curr_step < agent_args['history_length']:
            img, meas, rwrd, term = simulator.step(np.squeeze(ag.random_actions(1)).tolist())
        else:
            state_imgs = np.transpose(np.reshape(img_buffer[np.arange(curr_step-agent_args['history_length'], curr_step) % agent_args['history_length']], (1,) + agent_args['state_imgs_shape']), [0,2,3,1])
            state_meas = np.reshape(meas_buffer[np.arange(curr_step-agent_args['history_length'], curr_step) % agent_args['history_length']], (1,agent_args['history_length']*simulator.num_meas))

            curr_act = np.squeeze(ag.act(state_imgs, state_meas, agent_args['test_objective_params'])[0]).tolist()
            if curr_act[:6] in acts_to_replace:
                curr_act = replacement_act
            img, meas, rwrd, term = simulator.step(curr_act)
            if (not (meas is None)) and meas[0] > 30.:
                meas[0] = 30.
            
        if not term:
            img_buffer[curr_step % agent_args['history_length']] = img
            meas_buffer[curr_step % agent_args['history_length']] = meas
            curr_step += 1
                
    simulator.close_game()


if __name__ == '__main__':
    main()
