import pandas as pd
import json
import os
import tempfile
import sys

# Add project root to path
sys.path.append('/Users/educifuentes/code/greenlab-censos')

from utilities.data_transformations.survey_processing import map_survey_personas

def test_map_survey_personas():
    # Create a dummy mapping
    mapping = {
        "escalas_comunes": {
            "si_no_nr_na": {
                "1": "Sí",
                "2": "No"
            },
            "dificultad_salud": {
                "1": "Sin dificultad",
                "2": "Mucha dificultad"
            }
        },
        "mapeo_variables": {
            "sexo": {
                "1": "Hombre",
                "2": "Mujer"
            },
            "p48_anio_nac_uh": {
                "99": "No responde"
            }
        }
    }
    
    # Create a dummy dataframe
    df = pd.DataFrame({
        "p15_some_col": [1, 2, 1, 2],
        "p32a_vision": [1, 2, 1, 2],
        "p32g_invalid": [1, 2, 1, 2], # Should not be mapped by difficulty scale (only a-f)
        "sexo": [1, 2, 1, 2],
        "p48_anio_nac_uh": [1990, 2000, 99, 1800] # 1800 is out of range, should map if allowed or keep? Logic keeps if map fails?
    })
    
    # Create a temporary file for the mapping
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as tmp:
        json.dump(mapping, tmp)
        tmp_path = tmp.name
        
    try:
        # Run the transformation
        processed_df = map_survey_personas(df, tmp_path)
        
        # Verify p15 (Si/No)
        print("Checking p15...")
        assert processed_df["p15_some_col"].iloc[0] == "Sí"
        assert processed_df["p15_some_col"].iloc[1] == "No"
        
        # Verify p32 (Difficulty)
        print("Checking p32...")
        assert processed_df["p32a_vision"].iloc[0] == "Sin dificultad"
        
        # Verify p32g (Should NOT use difficulty scale)
        print("Checking p32g (should be unmapped)...")
        # Assuming unmapped columns are kept as original values
        assert processed_df["p32g_invalid"].iloc[0] == 1 
        
        # Verify standard mapping
        print("Checking Standard Mapping...")
        assert processed_df["sexo"].iloc[0] == "Hombre"
        
        # Verify p48 logic
        print("Checking p48...")
        assert str(processed_df["p48_anio_nac_uh"].iloc[0]) == "1990" # In range
        assert str(processed_df["p48_anio_nac_uh"].iloc[1]) == "2000" # In range
        assert processed_df["p48_anio_nac_uh"].iloc[2] == "No responde" # Code 99
        
        # 1800 is out of range [1934, 2024] and NOT in mapping. Logic says fillna with original.
        assert str(processed_df["p48_anio_nac_uh"].iloc[3]) == "1800" 
        
        print("✅ All tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        # Print df state for debugging
        if 'processed_df' in locals():
            print(processed_df)
    finally:
        os.remove(tmp_path)

if __name__ == "__main__":
    test_map_survey_personas()
