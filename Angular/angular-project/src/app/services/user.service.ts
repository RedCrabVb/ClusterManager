import { Injectable } from '@angular/core'
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http'
import { ConfigApp } from '../services/config'

@Injectable({
    providedIn: 'root'
})
export class UserService {
    constructor(private http: HttpClient, private config: ConfigApp) {

    }

    login(username: string | null, password: string | null) {

        let headers = new HttpHeaders({
            'Content-Type': 'application/x-www-form-urlencoded'
        });

        return this.http.post(
            this.config.urlBackEnd + 'token', `grant_type=password&username=${username}&password=${password}`, { headers: headers }
        )
    }
}