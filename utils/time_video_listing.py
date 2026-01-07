from pathlib import Path
from moviepy import VideoFileClip
import datetime

def gerar_lista_tempos(diretorio):
    pasta = Path(diretorio)
    
    arquivo_txt = pasta / "lista_tempos.txt"
    
    if not pasta.exists():
        print(f"Putz, não achei o diretório: {diretorio}")
        return

    print(f"Lendo os vídeos em: {pasta}...\nIsso pode demorar um pouquinho se tiver muito arquivo.\n")

    with open(arquivo_txt, 'w', encoding='utf-8') as f:
        
        f.write(f"RELATÓRIO DE AULAS - {datetime.datetime.now().strftime('%d/%m/%Y')}\n")
        f.write("-" * 50 + "\n\n")

        lista_videos = sorted(pasta.glob("*.mp4"))
        
        for video in lista_videos:
            try:
                clip = VideoFileClip(str(video))
                duracao_seg = clip.duration
                
                tempo_formatado = str(datetime.timedelta(seconds=int(duracao_seg)))
                
                linha = f"{video.name} \t{tempo_formatado}\n"
                f.write(linha)
                print(f"Processado: {video.name}")
                
                clip.close()
                
            except Exception as e:
                erro = f"ERRO ao ler {video.name}: {e}\n"
                f.write(erro)
                print(erro)


    print(f"\nShow! Arquivo salvo em: {arquivo_txt}")

caminho_da_pasta = r'/home/pedro/Videos/Aula 06'
gerar_lista_tempos(caminho_da_pasta)
