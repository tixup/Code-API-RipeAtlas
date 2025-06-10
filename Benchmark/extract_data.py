def find_german_probe_measurements(german_probes, measurements):
    """Trova misurazioni con probe tedeschi"""
    valid_measurements = []
    
    for measurement in measurements:
        try:
            # Ottieni i risultati con timeout piu' corto
            results_url = f"{BASE_URL}measurements/{measurement['id']}/results/?limit=100"
            response = requests.get(results_url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # Cerca probe tedeschi nei risultati
            for result in response.json():
                if isinstance(result, dict) and "prb_id" in result:
                    prb_id = int(result["prb_id"])
                    if prb_id in german_probes:
                        valid_measurements.append((measurement["id"], prb_id))
                        
                        # Interrompi se raggiunto il limite
                        if len(valid_measurements) >= MAX_MEASUREMENTS:
                            return valid_measurements
                        
            # Piccola pausa tra le richieste
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Errore analisi misurazione {measurement['id']}: {str(e)}")
            continue
    
    return valid_measurements