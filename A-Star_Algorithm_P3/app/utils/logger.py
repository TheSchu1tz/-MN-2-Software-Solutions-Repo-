from datetime import datetime
from pathlib import Path
from app.components.data_types.coordinate import Coordinate

class Logger:
    start:datetime
    filename = ""
    out_dir = Path("p3_logs")

    def __init__(self):
        self.start = datetime.now()
        self.filename = (
                f"KeoghsPort"
                f"{self.start.month:02d}_{self.start.day:02d}_{self.start.year}_"
                f"{self.start.hour:02d}{self.start.minute:02d}.txt"
        )
        
        self.out_dir.mkdir(parents=True, exist_ok=True)
        with open(self.out_dir / self.filename, "w") as log_file:
            log_file.write(f"{self.GetTime()} Program was started.\n")
        log_file.close()
    
    def LogManifestStart(self, manifest:str, numContainers:int):

        # Renames log file to have manifest name instead of "KeoghsPort", comment out if not needed
        manifest_name = Path(manifest).stem
        new_filename = (
            f"{manifest_name}_"
            f"{self.start.month:02d}_{self.start.day:02d}_{self.start.year}_"
            f"{self.start.hour:02d}{self.start.minute:02d}.txt"
        )

        current_file = self.out_dir / self.filename
        new_file = self.out_dir / new_filename

        if current_file.exists() and current_file != new_file:
            current_file.rename(new_file)
            self.filename = new_filename
        # End of renaming log file, comment out if not needed
        
        with open(self.out_dir / self.filename, "a") as log_file:
            log_file.write(f"{self.GetTime()} Manifest {manifest} is opened, there are {numContainers} containers on the ship.\n")
        log_file.close()

    def LogSolutionFound(self, moves:int, minutes:int):
        with open(self.out_dir / self.filename, "a") as log_file:
            log_file.write(f"{self.GetTime()} Balance solution found, it will require {moves} moves/{minutes} minutes.\n")
        log_file.close()

    def LogMove(self, coord1, coord2):
        with open(self.out_dir / self.filename, "a") as log_file:
            log_file.write(f"{self.GetTime()} {coord1} was moved to {coord2}\n")
        log_file.close()

    def LogMessage(self, message:str):
        with open(self.out_dir / self.filename, "a") as log_file:
            log_file.write(f"{self.GetTime()} {message}\n")
        log_file.close()
    
    def LogCycleEnd(self, outboundManifest:str):
        with open(self.out_dir / self.filename, "a") as log_file:
            log_file.write(f"{self.GetTime()} Finished a Cycle. Manifest {outboundManifest} was written to desktop, and a reminder pop-up to operator to send file was displayed.\n")
        log_file.close()

    def GetTime(self):
        time = datetime.now()
        return(f"{time.month:02d} {time.day:02d} {time.year}: "
                f"{time.hour:02d}:{time.minute:02d}")

    def WriteSessionLog(self):
        out_dir = Path("p3_logs")
        out_dir.mkdir(parents=True, exist_ok=True)
        with open(out_dir / self.filename, "a") as log_file:
            end = datetime.now()
            log_file.write(f"{self.GetTime()} Program was shut down.")
        log_file.close()