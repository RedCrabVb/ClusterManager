import { Component, Input } from '@angular/core';
import { InitFileService } from '../../services/initfile.service';
import { InitFile as data } from '../../date/initfile';
import { ModalService } from 'src/app/components/modal/modalService';
import { IInitFile } from 'src/app/date/IInitfile';
import { HttpErrorResponse } from '@angular/common/http';
import { catchError, throwError } from 'rxjs';

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
