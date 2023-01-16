import { Injectable } from '@angular/core'
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http'
import { ConfigApp } from '../services/config'

@Injectable({
    providedIn: 'root'
})
export class InitFileService {
    constructor(private http: HttpClient, private config: ConfigApp) {

    }

    // todo: limit version
    uploadFile(namefile: string, data: string, name: string) {
        // let body = new HttpParams()
        // .set('namefile', namefile)
        // .set('data', data)
        // .set('name', name);

        // let headers = new Headers();
        //   let requestOptions = new RequestOptions({headers});
        let headers = new HttpHeaders({
            'Content-Type': 'application/json'
        });
        let options = { headers: headers, body: {namefile, data, name} };

          
        return this.http.post(
            this.config.urlBackEnd + 'upload/initfile/test', {namefile, data, name}
        );
    }

    get() {
        return this.http.get(this.config.urlBackEnd)
    }
}