import CONST
import pandas as pd




def case_preprocessing(nou_cas):
    """
    Funció de preprocessament per al cas al qual se li ha de fer una recomanació.
    
    nou_cas: instància de Pandas amb el nou cas.

    """
    if float(nou_cas['edad'][0]) > 25:
        nou_cas['edad'][0] = CONST.edad[2]
    elif float(nou_cas['edad'][0]) < 12:
        nou_cas['edad'][0] = CONST.edad[0]
    else:
        nou_cas['edad'][0] = CONST.edad[1]
        
    
    columnas_categoricas = ['genero','edad','region','trabajo','musica','tarde_libre','vacaciones','mobilidad_reducida','longitud_ruta','sector']
    for col in columnas_categoricas:
        nou_cas = pd.get_dummies(nou_cas, columns=[col], prefix=col)
        
    for col in nou_cas.columns:
        if nou_cas[col].dtype == 'bool':
            nou_cas[col] = nou_cas[col].astype(int)

    return nou_cas


def find_cluster(nou_cas,loaded_scaler,loaded_kmeans,loaded_pca, path=''):
    """
    Troba el cluster del nou cas.

    nou_cas: instància de Pandas amb el nou_cas previament preprocessat.
    path: ubicació del directori amb els models
    """
    llista_aux = [0 for _ in range(len(CONST.subset_vars_list))]
    for var in range(len(CONST.subset_vars_list)):
        if CONST.subset_vars_list[var] not in nou_cas.columns:
            llista_aux[var] = 0
        else:
            llista_aux[var] = 1
            
    
            
    df = pd.DataFrame([llista_aux], columns=CONST.subset_vars_list)


    new_data_point = loaded_scaler.transform(df)
    

    
    principal_components = loaded_pca.transform(new_data_point)
    new_cluster = loaded_kmeans.predict(principal_components)
    
    return int(new_cluster)