import { Component, Input } from '@angular/core';
import { InitFileService } from '../../services/initfile.service';

@Component({
  selector: 'app-welcome',
  templateUrl: './welcome.page.component.html',
})
export class WelcomeComponent {

  constructor(private initFileService: InitFileService) {

  }

  sendInitFile() {

  }
}
