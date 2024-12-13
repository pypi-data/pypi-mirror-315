import os
import mne
import copy
import numpy as np
import scipy.signal as signal
import pandas as pd
import matplotlib.pyplot as plt
from bids import BIDSLayout
from APPLEE.functions import (run_ica,run_wicalp, reject, removeMuscle, noisy_channel,periodogram,run_wavelet)
from sovaflow.flow import (organize_channels,standardize, set_montage,run_reject) #run_prep
from APPLEE.Utils.utils import write_to_excel
from APPLEE.pipeline_stages.mypyprep import run_prep
from sovaflow.utils import cfg_logger, createRaw
from sovaharmony.preprocessing import write_json,get_derivative_path
from sovaharmony.info import info as info_dict
from APPLEE.pipeline_stages.linearFIR import filter_design
from datetime import datetime
from bids.layout import parse_file_entities


def preprocessing_ld(THE_DATASET,
          resample = None,
          reduction_channels= list,
          ica_method='infomax',
          montage_kind='standard_1005',
          fun_names_map=standardize,
          L_FREQ = 4,
          H_FREQ = 50,
          prep=False,
          path_save=str,
          score_muscle=0.7,
          ransac=False,
          correlation_secs=1.0,
          correlation_threshold=0.2,
          frac_bad=0.05,
          epoch_reject=5
          ):
    # Verificar si la carpeta existe y crearla si no existe
    if not os.path.exists(path_save):
      os.makedirs(path_save)
    # Dataset dependent inputs
    input_path = THE_DATASET.get('input_path',None)
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
  
    if montage_kind == 'standard_1005':
        default_channels = ['AF3',	'AF4',	'C1',	'C2',	'C3',	'C4',	'C5',	'C6',	'CP1',	'CP2',	'CP3',	'CP4',	'CP5',	'CP6',	'CPZ',	'CZ',	'F1',	'F2',	'F3',	'F4',	'F5',	'F6',	'F7',	'F8',	'FC1',	'FC2',	'FC3',	'FC4',	'FC5',	'FC6',	'FP1',	'FP2',	'FZ',	'O1',	'O2',	'OZ',	'P1',	'P2',	'P3',	'P4',	'P5',	'P6',	'P7',	'P8',	'PO3',	'PO4',	'PO7',	'PO8',	'POZ',	'PZ','T5','T6'	,'T7',	'T8',	'TP7',	'TP8'] #Yorguin
    if montage_kind == 'biosemi128':
        default_channels =  ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20', 'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28', 'A29', 'A30', 'A31', 'A32', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12', 'B13', 'B14', 'B15', 'B16', 'B17', 'B18', 'B19', 'B20', 'B21', 'B22', 'B23', 'B24', 'B25', 'B26', 'B27', 'B28', 'B29', 'B30', 'B31', 'B32', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 'C22', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30', 'C31', 'C32', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16', 'D17', 'D18', 'D19', 'D20', 'D21', 'D22', 'D23', 'D24', 'D25', 'D26', 'D27', 'D28', 'D29', 'D30', 'D31', 'D32']
    if prep:
      channels = THE_DATASET.get('channels',default_channels)
    else:
        channels = THE_DATASET.get('channels',reduction_channels)
        
    layout_dict = THE_DATASET.get('layout',None)
    # Static Params
    pipeline = 'APPLEE'
    pipelabel = '['+THE_DATASET.get('run-label', '')+']'
    layout = BIDSLayout(input_path)
    bids_root = layout.root
    output_path = os.path.join(bids_root,'derivatives',pipeline)

    eegs = layout.get(**layout_dict)
    derivatives_root = os.path.join(layout.root,'derivatives',pipeline)
    log_path = os.path.join(derivatives_root,'code')
    os.makedirs(log_path, exist_ok=True)
    logger,currentdt = cfg_logger(log_path)
    e = 0
    archivosconerror = []
    try:
      description = layout.get_dataset_description()
    except:
      description = {}
    desc_pipeline = "APPLEE, Automated Preprocessing Pipeline for Low-Electrode Encephalography using the bids standard"
    description['GeneratedBy']=[info_dict]
    write_json(description,os.path.join(derivatives_root,'dataset_description.json'))
    num_files = len(eegs)
  
    columnas = ["Row", "File_Length", "Number_User-Selected_Chans", 
            'bad_by_nan', 'bad_by_flat', 'bad_by_deviation', 'bad_by_hf_noise', 
            'bad_by_correlation', 'bad_by_SNR', 'bad_by_dropout', 'bad_by_ransac', 
            'bad_all',"Number_Good_Chans_Selected", "Percent_Good_Chans_Selected",
            'bad_after_by_nan', 'bad_after_by_flat', 'bad_after_by_deviation', 'bad_after_by_hf_noise', 
            'bad_after_by_correlation', 'bad_after_by_SNR', 'bad_after_by_dropout', 'bad_after_by_ransac', 
            'bad_after_all',"Number_after_Good_Chans_Selected", "Percent_after_Good_Chans_Selected",
            "score","correlation_threshold","frac_bad","comp_musc","epochs_non_reject"]

    # Crear un DataFrame vacío con las columnas especificadas
    QC_sujects=[]
    line_freqs = THE_DATASET['args']['line_freqs']
    for i,eeg_file in enumerate(eegs):
        try:
            logger.info(f"Parameters LEESOVA\nResample : {resample}\nica_method : {ica_method}\nMontage_kind : {montage_kind}")
            logger.info(f"Filter parameters\nL_FREQ : {L_FREQ}\nH_FREQ = {H_FREQ}")
            logger.info(f"Bad channerls parameters\ncorrelation_secs = {correlation_secs} \ncorrelation_threshold = {correlation_threshold}\nfrac_bad = {frac_bad}")
            logger.info(f"Muscle components parameters - ICA\nscore_muscle = {score_muscle}")
            logger.info(f"File {i+1} of {num_files} ({(i+1)*100/num_files}%) : {eeg_file}")
            
            param_id = f'sm{score_muscle}_ct{correlation_threshold}_fb{frac_bad}'
            
            prep_path = get_derivative_path(layout,eeg_file,'prep','eeg','.fif',bids_root,derivatives_root)
            wavelet_path = get_derivative_path(layout,eeg_file,'wavelet','eeg','.fif',bids_root,derivatives_root)
            stats_path = get_derivative_path(layout,eeg_file,'label','stats','.txt',bids_root,derivatives_root)
            wica_path = get_derivative_path(layout,eeg_file,'wica','eeg','.fif',bids_root,derivatives_root)
            reject_path = get_derivative_path(layout,eeg_file,'reject','eeg','.fif',bids_root,derivatives_root)
            Muscle_path = get_derivative_path(layout,eeg_file,f'Muscle_{param_id}','eeg','.fif',bids_root,derivatives_root)
            os.makedirs(os.path.split(wavelet_path)[0], exist_ok=True)
            
  
            json_dict = {"Description":desc_pipeline,"RawSources":[eeg_file.replace(bids_root,'')],"Configuration":THE_DATASET}
            json_dict["Sources"]=wavelet_path.replace(bids_root,'')
            
            raw_signal = mne.io.read_raw(eeg_file,preload=True)
            raw_signal = raw_signal.pick_types(eeg=True, meg=False, stim=False, eog=False, ecg=False, emg=False, misc=False)
            canales_a_eliminar = ['EKG', 'Photic']
            if set(canales_a_eliminar).intersection(raw_signal.ch_names):
                raw_signal.drop_channels(canales_a_eliminar)
            
            if all(elem in raw_signal.ch_names for elem in ['C29', 'C16', 'D19', 'B22', 'A15', 'A28', 'D31', 'B11']):
                montage_kind = 'biosemi128'
            info_raw=[os.path.basename(eeg_file),raw_signal.get_data().shape[1],raw_signal.get_data().shape[0]]
            
            if resample is not None:
                logger.info('Fs original: '+str(raw_signal.info['sfreq']))
                raw_signal = raw_signal.resample(resample, npad='auto', verbose='error') # To not get out of memory on RANSAC
                fs=resample
            
            if prep:
                if os.path.isfile(prep_path):
                    
                    logger.info(f'{wavelet_path} already existed, skipping...')
                else:
                    correct_montage = copy.deepcopy(channels)
                    raw,correct_montage= organize_channels(raw_signal,correct_montage,fun_names_map)
                    raw,montage = set_montage(raw,montage_kind)
                    prep = run_prep(raw,line_freqs,montage)
                    raw_signal = prep.raw.copy()
                    prep_info ={'noisy_channels_original':prep.noisy_channels_original,
                              'noisy_channels_before_interpolation':prep.noisy_channels_before_interpolation,
                              'noisy_channels_after_interpolation':prep.noisy_channels_after_interpolation,
                              'bad_before_interpolation':prep.bad_before_interpolation,
                              'interpolated_channels':prep.interpolated_channels,
                              'still_noisy_channels':prep.still_noisy_channels,
                              }
                    raw_signal.save(prep_path ,split_naming='bids', overwrite=True)
                    write_json(json_dict,prep_path.replace('.fif','.json'))
                    write_json(json_dict,stats_path.replace('label','prep').replace('.txt','.json'))
                    write_json(prep_info,stats_path.replace('label','prep'))
            
            info_before_noisy=list(noisy_channel(raw_signal,ransac=ransac, correlation_secs=correlation_secs, correlation_threshold=correlation_threshold, frac_bad=frac_bad).values())
            info_raw.extend(info_before_noisy)
            bad_all=len(info_raw[-1])
            info_raw.append(info_raw[2]-bad_all)
            info_raw.append(((info_raw[2]-bad_all)/info_raw[2])*100)
            
            if os.path.isfile(wavelet_path) :
                logger.info(f'{wavelet_path} already existed, skipping...')
            else:
                if prep:
                    raw = mne.io.read_raw(prep_path,preload=True)
                else:
                    raw=raw_signal.copy()
                if montage_kind == 'biosemi128':    
                  try:
                    raw.pick_channels(ch_names=['C29', 'C16', 'D19', 'B22', 'A15', 'A28', 'D31', 'B11'])  
                    rename_dict = {'C29': 'FP1', 'C16': 'FP2', 'D19': 'C3', 'B22': 'C4','A15':'O1','A28':'O2','D31':'P7','B11':'P8'}
                    raw.rename_channels(rename_dict)
                    montage_kind = 'standard_1005'
                  except:
                    print('No rename channels')
                else:
                    raw.pick_channels(ch_names=reduction_channels) 
                correct_montage = copy.deepcopy(reduction_channels)
                raw,correct_montage= organize_channels(raw,correct_montage,fun_names_map)
                raw,montage = set_montage(raw,montage_kind)
                if correct_montage is not None:
                  assert correct_montage == set(raw.info['ch_names'])
                
                wavelet_signal=run_wavelet(raw,fs=raw.info['sfreq'],L_FREQ = L_FREQ,H_FREQ = H_FREQ)
                wavelet_signal.save(wavelet_path ,split_naming='bids', overwrite=True)
                write_json(json_dict,wavelet_path.replace('.fif','.json'))
                
  
            if os.path.isfile(wica_path) :
                logger.info(f'{wavelet_path} already existed, skipping...')
            else:
                signal = mne.io.read_raw(wavelet_path,preload=True)
                S,A,W,pca_mean,pre_whitener,_ = run_ica(signal,None,ica_method,show=False)
                wica_signal,wica_info = run_wicalp(S,A,pca_mean,pre_whitener,signal.info['sfreq'],ica_method,signal.info['ch_names'],h_freq=50,epoch_length=5)
                wica_signal.save(wica_path ,split_naming='bids', overwrite=True)
                write_json(json_dict,wica_path.replace('.fif','.json'))
                write_json(wica_info,stats_path.replace('label','wica'+pipelabel))
                
  
            if os.path.isfile(reject_path) :
                logger.info(f'{wavelet_path} already existed, skipping...')
            else:
                signal = mne.io.read_raw(wica_path,preload=True)
                try:
                  reject_signal,reject_info, epochs_reject = reject(signal, mode='autorej',epoch_length=epoch_reject)
                  reject_signal.save(reject_path ,split_naming='bids', overwrite=True)
                  
                  write_json(json_dict,reject_path.replace('.fif','.json'))
                  write_json(json_dict,stats_path.replace('label','reject'+pipelabel).replace('.txt','.json'))
                  
                  write_json(reject_info,stats_path.replace('label','reject'+pipelabel))
                except:
                  print(f'No reject in {wica_path}')
  
                
            if os.path.isfile(Muscle_path):
                logger.info(f'{wavelet_path} already existed, skipping...')
                
            else:
                signal = mne.io.read_raw(reject_path,preload=True)
                raw = signal.copy() #raw = read_raw(filename, preload=True)#mne_open(filename)
                raw,correct_montage= organize_channels(raw,raw.info.ch_names,fun_names_map)
                raw,montage = set_montage(raw,montage_kind)
                if correct_montage is not None:
                 assert correct_montage == set(raw.info['ch_names'])
                reconst_raw,comp_musc=removeMuscle(raw, score= score_muscle ,ica_method=ica_method,verbose=False)
                info_noisy=noisy_channel(reconst_raw,ransac=ransac, correlation_secs=correlation_secs, correlation_threshold=correlation_threshold, frac_bad=frac_bad)
                 
                info_after_noisy=list(info_noisy.values())
                info_raw.extend(info_after_noisy)
                bad_all=len(info_raw[-1])
                info_raw.append(info_raw[2]-bad_all)
                info_raw.append(((info_raw[2]-bad_all)/info_raw[2])*100)
                info_raw.append(score_muscle)
                info_raw.append(correlation_threshold)
                info_raw.append(frac_bad)
                info_raw.append(comp_musc)
                info_raw.append(epochs_reject)
                QC_sujects.append(info_raw)
                 
                logger.info(f'{info_noisy}')
                reconst_raw.save(Muscle_path ,split_naming='bids', overwrite=True)
                write_json(json_dict,Muscle_path.replace('.fif','.json'))
                write_json(info_noisy,stats_path.replace('label','Muscle'+pipelabel))
                print('Done Muscle noisy detect')
            
          
        except Exception as error:
            e+=1
            logger.exception(f'Error for {eeg_file}')
            archivosconerror.append(eeg_file)
            print(error)
            pass
    df_QC = pd.DataFrame(QC_sujects,columns=columnas)
    df_QC = df_QC.applymap(lambda x: 0 if x == [] else x)
    task=THE_DATASET.get('layout')['task']
    write_to_excel(df_QC, fr'{path_save}\QC_{THE_DATASET["name"]}.xlsx',sheet_name=f'{param_id}_{task}')
    print("Save... Quality control")



