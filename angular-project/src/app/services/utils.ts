import { HttpErrorResponse } from "@angular/common/http";
import { throwError } from "rxjs";
import Swal from "sweetalert2";

export class Utils {
    static getCookie(name: string) {
        let ca: Array<string> = document.cookie.split(';');
        let caLen: number = ca.length;
        let cookieName = `${name}=`;
        let c: string;

        for (let i: number = 0; i < caLen; i += 1) {
            c = ca[i].replace(/^\s+/g, '');
            if (c.indexOf(cookieName) == 0) {
                return c.substring(cookieName.length, c.length);
            }
        }
        return '';
    }

    static handleError(error: HttpErrorResponse) {
        if (error.status === 0) {
            console.error('An error occurred:', error.error);
            // alert('An error occurred: ' + error.message);
            Swal.fire('Error', 'An error occurred: ' + error.message, 'error')
        } else {
            console.error(
                `Backend returned code ${error.status}, body was: `, error.error);

            Swal.fire('Error', `Backend returned code ${error.status}, body was: ` + error.message, 'error');
        }
        return throwError(() => new Error('Something bad happened; please try again later.'));
    }
}
