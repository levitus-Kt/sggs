import getpass

user = "/home/" + getpass.getuser()

class FileRevealer:
    def __init__(self, title, list):
        self.title = title
        self.list = list

        
    def default(self):
        with open(f"{user}/sggs/ringer/wav/storage/default/bell-classic-pre.wav", "wb+") as destination:
            for chunk in self.list[0].chunks():     # Зацикливание на chunks() не перегрузит память системы большими файлами
                destination.write(chunk)
        
        with open(f"{user}/sggs/ringer/wav/storage/default/bell-classic-in.wav", "wb+") as destination:
            for chunk in self.list[1].chunks():
                destination.write(chunk)
        
        with open(f"{user}/sggs/ringer/wav/storage/default/bell-classic-out.wav", "wb+") as destination:
            for chunk in self.list[2].chunks():
                destination.write(chunk)

        return 0
    

    def twentyThirdFeb(self):
        with open(f"{user}/sggs/ringer/wav/storage/23.02-pre.wav", "wb+") as destination:
            for chunk in self.list[0].chunks():
                destination.write(chunk)
        
        with open(f"{user}/sggs/ringer/wav/storage/23.02-in.wav", "wb+") as destination:
            for chunk in self.list[1].chunks():
                destination.write(chunk)
        
        with open(f"{user}/sggs/ringer/wav/storage/23.02-out.wav", "wb+") as destination:
            for chunk in self.list[2].chunks():
                destination.write(chunk)

        return 0


    def eighthMar(self):
        with open(f"{user}/sggs/ringer/wav/storage/8.03-pre.wav", "wb+") as destination:
            for chunk in self.list[0].chunks():
                destination.write(chunk)
        
        with open(f"{user}/sggs/ringer/wav/storage/8.03-in.wav", "wb+") as destination:
            for chunk in self.list[1].chunks():
                destination.write(chunk)
        
        with open(f"{user}/sggs/ringer/wav/storage/8.03-out.wav", "wb+") as destination:
            for chunk in self.list[2].chunks():
                destination.write(chunk)

        return 0


    def firstMay(self):
        with open(f"{user}/sggs/ringer/wav/storage/1.05-pre.wav", "wb+") as destination:
            for chunk in self.list[0].chunks():
                destination.write(chunk)
        
        with open(f"{user}/sggs/ringer/wav/storage/1.05-in.wav", "wb+") as destination:
            for chunk in self.list[1].chunks():
                destination.write(chunk)
        
        with open(f"{user}/sggs/ringer/wav/storage/1.05-out.wav", "wb+") as destination:
            for chunk in self.list[2].chunks():
                destination.write(chunk)

        return 0

    
    def ninthMay(self):
        with open(f"{user}/sggs/ringer/wav/storage/9.05-pre.wav", "wb+") as destination:
            for chunk in self.list[0].chunks():
                destination.write(chunk)
        
        with open(f"{user}/sggs/ringer/wav/storage/9.05-in.wav", "wb+") as destination:
            for chunk in self.list[1].chunks():
                destination.write(chunk)
        
        with open(f"{user}/sggs/ringer/wav/storage/9.05-out.wav", "wb+") as destination:
            for chunk in self.list[2].chunks():
                destination.write(chunk)

        return 0

    
    def firstSep(self):
        with open(f"{user}/sggs/ringer/wav/storage/1.09-pre.wav", "wb+") as destination:
            for chunk in self.list[0].chunks():
                destination.write(chunk)
        
        with open(f"{user}/sggs/ringer/wav/storage/1.09-in.wav", "wb+") as destination:
            for chunk in self.list[1].chunks():
                destination.write(chunk)
        
        with open(f"{user}/sggs/ringer/wav/storage/1.09-out.wav", "wb+") as destination:
            for chunk in self.list[2].chunks():
                destination.write(chunk)

        return 0
    
    
    def halloween(self):
        with open(f"{user}/sggs/ringer/wav/storage/hallo-pre.wav", "wb+") as destination:
            for chunk in self.list[0].chunks():
                destination.write(chunk)
        
        with open(f"{user}/sggs/ringer/wav/storage/hallo-in.wav", "wb+") as destination:
            for chunk in self.list[1].chunks():
                destination.write(chunk)
        
        with open(f"{user}/sggs/ringer/wav/storage/hallo-out.wav", "wb+") as destination:
            for chunk in self.list[2].chunks():
                destination.write(chunk)

        return 0
    

    def fourthNov(self):
        with open(f"{user}/sggs/ringer/wav/storage/gymn-pre.wav", "wb+") as destination:
            for chunk in self.list[0].chunks():
                destination.write(chunk)
        
        with open(f"{user}/sggs/ringer/wav/storage/gymn-in.wav", "wb+") as destination:
            for chunk in self.list[1].chunks():
                destination.write(chunk)
        
        with open(f"{user}/sggs/ringer/wav/storage/gymn-out.wav", "wb+") as destination:
            for chunk in self.list[2].chunks():
                destination.write(chunk)

        return 0

    
    def new_year(self):
        with open(f"{user}/sggs/ringer/wav/storage/default/bell-ny-pre.wav", "wb+") as destination:
            for chunk in self.list[0].chunks():
                destination.write(chunk)
        
        with open(f"{user}/sggs/ringer/wav/storage/default/bell-ny-in.wav", "wb+") as destination:
            for chunk in self.list[1].chunks():
                destination.write(chunk)
        
        with open(f"{user}/sggs/ringer/wav/storage/default/bell-ny-out.wav", "wb+") as destination:
            for chunk in self.list[2].chunks():
                destination.write(chunk)

        return 0


    def matched(self):
        match self.title:
            case "default": return self.default()
            case "23feb": return self.twentyThirdFeb()
            case "8mar": return self.eighthMar()
            case "1may": return self.firstMay()
            case "9may": return self.ninthMay()
            case "1sep": return self.firstSep()
            case "halloween": return self.halloween()
            case "4nov": return self.fourthNov()
            case "ny": return self.new_year()
