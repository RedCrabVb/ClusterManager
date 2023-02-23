import { Component, Input } from '@angular/core';
import { InitFileService } from '../../services/initfile.service';
import { InitFile as data } from '../../date/initfile';
import { ModalService } from 'src/app/components/modal/modalService';
import { IInitFile } from 'src/app/date/IInitfile';
import { HttpErrorResponse } from '@angular/common/http';
import { catchError, throwError } from 'rxjs';
import { FormControl } from '@angular/forms';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'app-welcome',
  templateUrl: './welcome.page.component.html',
})
export class WelcomeComponent {
  newPassword: FormControl = new FormControl('')

  constructor(private userService: UserService) {

  }

  updatePassword() {
    this.userService.updatePassword(this.newPassword.value).subscribe((res: any) => {
      console.log(res);
      alert(res.Status);
      window.location.href = '/login';
    });
  }
}
