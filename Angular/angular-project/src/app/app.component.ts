import { Component, Input } from '@angular/core';
import { InitFileService } from './services/initfile.service'; 

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  sendInitFile() {
    console.log('Click me!')
  }
}
