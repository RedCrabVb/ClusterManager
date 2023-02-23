import { Injectable } from '@angular/core'
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http'
import { ConfigApp } from '../services/config'
import { Utils } from './utils';

@Injectable({
    providedIn: 'root'
})
export class UserService {
    constructor(private http: HttpClient, private config: ConfigApp) {

    }

    getAuthHeader() {
        let headers = new HttpHeaders({
            'Authorization': `${Utils.getCookie('token_type')} ${Utils.getCookie('access_token')}`
        });

        return {headers: headers};
    }


    login(username: string | null, password: string | null) {

        let headers = new HttpHeaders({
            'Content-Type': 'application/x-www-form-urlencoded'
        });

        return this.http.post(
            this.config.urlBackEnd + 'token', `grant_type=password&username=${username}&password=${password}`, { headers: headers }
        );
    }

    updatePassword(newPassword: string) {
        let headers = new HttpHeaders({
            'Content-Type': 'application/x-www-form-urlencoded'
        });

        return this.http.post(
            this.config.urlBackEnd + 'update_password?new_password=' + newPassword, {}, this.getAuthHeader()
        );
    }
}