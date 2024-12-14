from loguru import logger
from pydub import AudioSegment


def mp3(src: str, dst: str) -> None:
    dst_format = dst.split(".")[-1]

    if dst_format == "wav":
        mp3_to_wav(src, dst)
    elif dst_format == "m4a":
        mp3_to_m4a(src, dst)
    else:
        logger.error(f"Unsupported format {dst_format}")
    return


def mp3_to_wav(src: str, dst: str) -> None:
    audio = AudioSegment.from_mp3(src)
    audio.export(dst, format="wav")
    return


def mp3_to_m4a(src: str, dst: str) -> None:
    audio = AudioSegment.from_mp3(src)
    audio.export(dst, format="ipod")
    return


def m4a(src: str, dst: str) -> None:
    dst_format = dst.split(".")[-1]

    if dst_format == "wav":
        m4a_to_wav(src, dst)
    elif dst_format == "mp3":
        m4a_to_mp3(src, dst)
    else:
        logger.error(f"Unsupported format {dst_format}")
    return


def m4a_to_wav(src: str, dst: str) -> None:
    audio = AudioSegment.from_file(src, format="m4a")
    audio.export(dst, format="wav")
    return


def m4a_to_mp3(src: str, dst: str) -> None:
    audio = AudioSegment.from_file(src, format="m4a")
    audio.export(dst, format="mp3")
    return
