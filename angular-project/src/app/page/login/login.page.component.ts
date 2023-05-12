import { Component, Input } from '@angular/core';
import { UserService } from '../../services/user.service';
import { FormControl } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';
import { catchError, throwError } from 'rxjs';
import { Router } from '@angular/router';
import Swal from 'sweetalert2';

@Component({
    selector: 'app-login',
    templateUrl: './login.page.component.html',
})
export class LoginComponent {

    passwordFild = new FormControl('');
    usernameFild = new FormControl('');

    constructor(private userService: UserService, private router: Router) {
        this.deleteCookie('access_token');
        this.deleteCookie('token_type');
    }

    private deleteCookie(name: string) {
        this.setCookie(name, '', -1);
    }

    private setCookie(name: string, value: string, expireDays: number, path: string = '') {
        let d: Date = new Date();
        d.setTime(d.getTime() + expireDays * 24 * 60 * 60 * 1000);
        let expires: string = `expires=${d.toUTCString()}`;
        let cpath: string = path ? `; path=${path}` : '';
        document.cookie = `${name}=${value}; ${expires}${cpath}`;
    }

    private handleError(error: HttpErrorResponse) {
        if (error.status === 0) {
            console.error('An error occurred:', error.error);
            Swal.fire('Error', 'Try a different username/password, check the availability of the server', 'error');
        } else {
            console.error(
                `Backend returned code ${error.status}, body was: `, error.error);

            Swal.fire('Error', `Backend returned code ${error.status}, body was: ` + error.message, 'error');
        }
        return throwError(() => new Error('Something bad happened; please try again later.'));
    }

    Login() {
        this.userService.login(this.usernameFild.value, this.passwordFild.value)
            .pipe(catchError(this.handleError))
            .subscribe((res: any) => {
                console.log(res);
                // Swal.fire('This is a simple and sweet alert')

                this.setCookie('access_token', res.access_token, 10);
                this.setCookie('token_type', res.token_type, 10);

                this.router.navigate([''])

            })
    }
}
