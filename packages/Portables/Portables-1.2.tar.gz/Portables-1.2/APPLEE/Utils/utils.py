import pandas as pd
import os 

def combine_sheets(excel_path, output_path):
    # Leer el archivo Excel
    xls = pd.ExcelFile(excel_path)
    
    # Crear una lista para almacenar los DataFrames de cada hoja
    df_list = []
    
    # Iterar a través de cada hoja en el archivo Excel
    for sheet_name in xls.sheet_names:
        # Leer la hoja
        df = pd.read_excel(xls, sheet_name=sheet_name)
        
        # Añadir una columna con el nombre de la hoja
        df['sheet_name'] = sheet_name
        
        # Añadir el DataFrame a la lista
        df_list.append(df)
    
    # Concatenar todos los DataFrames en uno solo
    combined_df = pd.concat(df_list, ignore_index=True)
    
    # Guardar el DataFrame combinado en un nuevo archivo Excel
    combined_df.to_excel(output_path, index=False)

def write_to_excel(df, path, sheet_name):
    if not os.path.exists(path):
        # Si el archivo no existe, crea un nuevo archivo con la primera hoja
        df.to_excel(path, sheet_name=sheet_name, index=False)
    else:
        # Si el archivo existe, abrelo en modo 'a' y añade la nueva hoja
        with pd.ExcelWriter(path, mode='a', engine='openpyxl',if_sheet_exists='overlay') as writer:
            try:
                existing_df = pd.read_excel(path, sheet_name=sheet_name)
                # Concatenar el nuevo DataFrame con el existente
                combined_df = pd.concat([existing_df, df], ignore_index=True)
                # Guarda el DataFrame combinado en la hoja
                combined_df.to_excel(writer, sheet_name=sheet_name, index=False)
            except ValueError:
                # Si la hoja no existe, simplemente escribe el DataFrame como nueva hoja
                df.to_excel(writer, sheet_name=sheet_name, index=False)


def plot_stage(THE_DATASET=dict,
               desired_order = ['FP1', 'FP2', 'C3', 'C4', 'P7', 'P8', 'O1', 'O2'],
               path_save=str,
               bands=dict,
               score_muscle=0.7,
               correlation_threshold=0.2,
               frac_bad=0.05,
               montage_kind='standard_1005',
               scale='V'):
    
    input_path = THE_DATASET.get('input_path',None)
    layout_dict = THE_DATASET.get('layout',None)
    e = 0
    archivosconerror = []
    # Static Params
    pipelabel = '['+THE_DATASET.get('run-label', '')+']'
    layout = BIDSLayout(input_path)
    bids_root = layout.root
    eegs = layout.get(**layout_dict)
    pipeline = 'APPLEE'
    derivatives_root = os.path.join(layout.root,'derivatives',pipeline)
    log_path = os.path.join(derivatives_root,'code')
    os.makedirs(log_path, exist_ok=True)
    logger,currentdt = cfg_logger(log_path)
    num_files = len(eegs)
    if montage_kind == 'standard_1005':
        default_channels = ['AF3',	'AF4',	'C1',	'C2',	'C3',	'C4',	'C5',	'C6',	'CP1',	'CP2',	'CP3',	'CP4',	'CP5',	'CP6',	'CPZ',	'CZ',	'F1',	'F2',	'F3',	'F4',	'F5',	'F6',	'F7',	'F8',	'FC1',	'FC2',	'FC3',	'FC4',	'FC5',	'FC6',	'FP1',	'FP2',	'FZ',	'O1',	'O2',	'OZ',	'P1',	'P2',	'P3',	'P4',	'P5',	'P6',	'P7',	'P8',	'PO3',	'PO4',	'PO7',	'PO8',	'POZ',	'PZ','T5','T6'	,'T7',	'T8',	'TP7',	'TP8'] #Yorguin
        channels = THE_DATASET.get('channels',default_channels)
    else:
        channels = THE_DATASET.get('channels',desired_order)
    # Get all combinations of the parameters


    for i,eeg_file in enumerate(eegs):
        info_bids_sujeto = parse_file_entities(eeg_file)
        #process=str(i)+'/'+str(num_files)
        msg =f"File {i+1} of {num_files} ({(i+1)*100/num_files}%) : {eeg_file}"
        logger.info(msg)
        
        param_id = f'sm{score_muscle}_ct{correlation_threshold}_fb{frac_bad}'
        
        wavelet_path = get_derivative_path(layout,eeg_file,'wavelet','eeg','.fif',bids_root,derivatives_root)
        wica_path = get_derivative_path(layout,eeg_file,'wica','eeg','.fif',bids_root,derivatives_root)
        reject_path = get_derivative_path(layout,eeg_file,'reject','eeg','.fif',bids_root,derivatives_root)
        DM_path = get_derivative_path(layout,eeg_file,f'Muscle_{param_id}','eeg','.fif',bids_root,derivatives_root)
       
        signal_uploaded=mne.io.read_raw(eeg_file)
        
        if  montage_kind == 'standard_1005':
            fun_names_map=standardize
            correct_montage = copy.deepcopy(channels)
            signal,correct_montage= organize_channels(signal_uploaded,correct_montage,fun_names_map)
            signal_uploaded,montage = set_montage(signal,montage_kind)
            signal_uploaded.pick_channels(ch_names=desired_order)
        if montage_kind == 'biosemi128':
            signal_uploaded.pick_channels(ch_names=['C29','C16','D19','B22','A15','A28','D31','B11'])
            rename_dict = {'C29': 'FP1', 'C16': 'FP2', 'D19': 'C3', 'B22': 'C4', 'A15': 'O1', 'A28': 'O2', 'D31': 'P7', 'B11': 'P8'}
            signal_uploaded.rename_channels(rename_dict)
            
            
        #signal_uploaded.resample(250, npad='auto', verbose='error') # To not get out of memory on RANSAC

        signal_wavelet = mne.io.read_raw(wavelet_path)
        signal_wica = mne.io.read_raw(wica_path)
        signal_reject=mne.io.read_raw(reject_path)
        try: 
            signal_DM = mne.io.read_raw(DM_path)
            
            def get_order_indices(signal_channels, desired_order):
                return [signal_channels.index(ch) for ch in desired_order if ch in signal_channels]

            raw_channels = signal_uploaded.info['ch_names']
            wavelet_channels = signal_wavelet.info['ch_names']
            wica_channels = signal_wica.info['ch_names']
            reject_channels = signal_reject.info['ch_names']
            reconst_channels = signal_DM.info['ch_names']

            raw_order = get_order_indices(raw_channels, desired_order)
            wavelet_order = get_order_indices(wavelet_channels, desired_order)
            wica_order = get_order_indices(wica_channels, desired_order)
            reject_order = get_order_indices(reject_channels, desired_order)
            reconst_order = get_order_indices(reconst_channels, desired_order)

            #raw_o = raw.get_data()[raw_order, :]
            wav_o = signal_wavelet.get_data()[wavelet_order, :] 
            wica_o = signal_wica.get_data()[wica_order, :]
            reject_o = signal_reject.get_data()[reject_order, :]
            dm_o= signal_DM.get_data()[reconst_order, :]
            num_rows=4
            fig, axs = plt.subplots(num_rows, 2, figsize=(15, 2*num_rows))
            row_index=0
            colors=['m','r','g','orange','b']
            for i,ch in enumerate(desired_order):
                row = row_index // 2  # Determina la fila del subplot
                col = row_index % 2
                #axs[row,col].plot(signal_uploaded.get_data()[i,:],label='raw',color=colors[0])
                #axs[row,col].plot(raw.get_data()[i,:],label='prep')
                #axs[row,col].plot(signal_wavelet.get_data()[i,:],label='wavelet',color=colors[1])
                #axs[row,col].plot(signal_wica.get_data()[i,:],label='wica',color=colors[2])
                #axs[row,col].plot(signal_reject.get_data()[i,:],label='reject',color=colors[3])
                axs[row,col].plot(dm_o[i,:],label='Muscle',color=colors[4], linestyle='--')
                axs[row, col].legend()
                row_index += 1
                axs[row, col].set_title(ch) 
            plt.tight_layout()

            fname='sub-'+ info_bids_sujeto['subject'] 
            task=info_bids_sujeto['task']
            fig.suptitle(fname)

            # Crear la ruta completa para la carpeta 'stages_pipeline'
            dir_path = os.path.join(path_save,'plot', 'stages_pipeline')

            # Verificar si la carpeta existe y crearla si no existe
            if not os.path.exists(fr'{dir_path}'):
                os.makedirs(dir_path)

            # Guardar el gráfico en la carpeta
            plt.savefig(os.path.join(dir_path,f'{fname}_{task}_{param_id}.png'))
            plt.close()

            #if prep:
                #pot_prep,ss_prep,ffo_prep=periodogram(raw.get_data(), raw.info['sfreq'], bands,all=True,channels=raw.info['ch_names'])

            pot,ss,ffo=periodogram(signal_uploaded.get_data(), signal_uploaded.info['sfreq'], bands,all=True,channels=signal_uploaded.info['ch_names'],scale=scale)
            pot_wav,ss_wav,ffo_wav=periodogram(signal_wavelet.get_data(), signal_wavelet.info['sfreq'], bands,all=True,channels=signal_wavelet.info['ch_names'],scale=scale)
            pot_wica,ss_wica,ffo_wica=periodogram(signal_wica.get_data(), signal_wica.info['sfreq'], bands,all=True,channels=signal_wica.info['ch_names'],scale=scale)
            pot_reject,ss_reject,ffo_reject=periodogram(signal_reject.get_data(), signal_reject.info['sfreq'], bands,all=True,channels=signal_reject.info['ch_names'],scale=scale)
            pot_dm,ss_dm,ffo_dm=periodogram(signal_DM.get_data(), signal_DM.info['sfreq'], bands,all=True,channels=signal_DM.info['ch_names'],scale=scale)
            name = 'sub-'+ info_bids_sujeto['subject'] 

            num_rows=4

            ss = np.array(ss)
            ss_wav = np.array(ss_wav)
            ss_wica = np.array(ss_wica)
            ss_reject = np.array(ss_reject)
            ss_dm = np.array(ss_dm)  
            ffo = np.array(ffo)
            ffo_wav = np.array(ffo_wav)
            ffo_wica = np.array(ffo_wica)
            ffo_reject = np.array(ffo_reject)
            ffo_dm = np.array(ffo_dm)  
            ss = ss[raw_order, :]
            ffo = ffo[raw_order, :]  
            ss_wav = ss_wav[wavelet_order, :]
            ffo_wav = ffo_wav[wavelet_order, :]  
            ss_wica = ss_wica[wica_order, :]
            ffo_wica = ffo_wica[wica_order, :]  
            ss_reject = ss_reject[reject_order, :]
            ffo_reject = ffo_reject[reject_order, :]  
            ss_dm = ss_dm[reconst_order, :]
            ffo_dm = ffo_dm[reconst_order, :]

            fig1, axs1 = plt.subplots(num_rows, 2, figsize=(15, 2*num_rows))
            row_index=0
            x_line = [6, 8.5, 10.5, 12.5, 18.5, 21, 30]
            colors=['m','r','g','orange','b']
            for i,ch in enumerate(desired_order):
                row = row_index // 2  # Determina la fila del subplot
                col = row_index % 2
                axs1[row,col].plot(ffo_wav[i],ss_wav[i],label='wavelet',color=colors[1])
                #if prep:
                    #axs1[row,col].plot(ffo_prep[i],ss_prep[i],label='prep')
                axs1[row,col].plot(ffo_wica[i],ss_wica[i],label='wica',color=colors[2])
                axs1[row,col].plot(ffo_reject[i],ss_reject[i],label='reject',color=colors[3])
                axs1[row,col].plot(ffo_dm[i],ss_dm[i],label='Muscle',color=colors[4])
                axs1[row, col].legend()
                axs1[row, col].set_title(ch)
                axs1[row, col].set_xlim(1.5, 50)
                row_index += 1
                for x in x_line:
                    axs1[row, col].axvline(x=x, color='gray', linestyle='--')
                plt.tight_layout()
            print('done periodogram')
            plt.tight_layout()
            fig1.suptitle(fname)

            # Crear la ruta completa para la carpeta 'stages_pipeline'
            dir_path = os.path.join(path_save, 'plot','multitaper')

            # Verificar si la carpeta existe y crearla si no existe
            if not os.path.exists(fr'{dir_path}'):
                os.makedirs(dir_path)

            # Guardar el gráfico en la carpeta
            plt.savefig(os.path.join(dir_path,f'{fname}_{task}_{param_id}.png'))
            plt.close()

        except:
            print('Es posible que el archivo no exista o hay un error realcionado con este')
            print(DM_path)
