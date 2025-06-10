def fetch_measurement_results(measurement_id, api_key):
    """Recupera e analizza i risultati di una misurazione specifica"""
    url = f"https://atlas.ripe.net/api/v2/measurements/{measurement_id}/results/"
    headers = {'Authorization': f'Key {api_key}'}
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        results = response.json()
        
        latencies = []
        for r in results:
            # Caso 1: RTT diretto nell'oggetto principale
            if isinstance(r.get('rtt'), (int, float)) and 0 < r['rtt'] < 10000:  # Filtro valori anomali
                latencies.append(r['rtt'])
            
            # Caso 2: RTT annidato in oggetto 'result'
            elif isinstance(r.get('result'), dict):
                if isinstance(r['result'].get('rtt'), (int, float)) and 0 < r['result']['rtt'] < 10000:
                    latencies.append(r['result']['rtt'])
            
            # Caso 3: Risultati in formato array (per misurazioni multi-pacchetto)
            elif isinstance(r.get('result'), list):
                for ping_result in r['result']:
                    if isinstance(ping_result.get('rtt'), (int, float)) and 0 < ping_result['rtt'] < 10000:
                        latencies.append(ping_result['rtt'])
        
        if not latencies:
            return None
            
        return {
            'avg': round(statistics.mean(latencies), 2),
            'min': min(latencies),
            'max': max(latencies),
            'samples': len(latencies),
            'packet_loss': calculate_packet_loss(results, latencies)
        }
        
    except Exception as e:
        print(f"Error processing measurement {measurement_id}: {str(e)}")
        return None