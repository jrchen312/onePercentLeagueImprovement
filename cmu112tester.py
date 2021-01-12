from cmu_112_graphics import *

class MyApp(App):
    def appStarted(self): 
        self.messages = ['appStarted']

    def appStopped(self):
        self.messages.append('appStopped')
        print('appStopped!')

    def keyPressed(self, event):
        self.messages.append('keyPressed: ' + event.key)

    def keyReleased(self, event):
        self.messages.append('keyReleased: ' + event.key)

    def mousePressed(self, event):
        self.messages.append(f'mousePressed at {(event.x, event.y)}')

    def mouseReleased(self, event):
        self.messages.append(f'mouseReleased at {(event.x, event.y)}')

    def mouseMoved(self, event):
        self.messages.append(f'mouseMoved at {(event.x, event.y)}')

    def mouseDragged(self, event):
        self.messages.append(f'mouseDragged at {(event.x, event.y)}')

    def sizeChanged(self):
        self.messages.append(f'sizeChanged to {(self.width, self.height)}')

    def mouseScrolled(self, event):
        print('scroll')
        self.messages.append(f'mouseScrolled by {(event.x, event.y)}')

    def redrawAll(self, canvas):
        font = 'Arial 20 bold'
        canvas.create_text(self.width/2,  30, text='Events Demo', font=font)
        n = min(10, len(self.messages))
        i0 = len(self.messages)-n
        for i in range(i0, len(self.messages)):
            canvas.create_text(self.width/2, 100+50*(i-i0),
                               text=f'#{i}: {self.messages[i]}',
                               font=font)

MyApp(width=600, height=600)