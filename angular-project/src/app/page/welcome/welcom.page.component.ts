import { Component, Input } from '@angular/core';
import { FormControl } from '@angular/forms';
import { UserService } from 'src/app/services/user.service';
import Swal from 'sweetalert2';

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
      Swal.fire('success', (res.Status), 'success');
      window.location.href = '/login';
    });
  }
}
