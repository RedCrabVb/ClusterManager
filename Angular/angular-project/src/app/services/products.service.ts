import { Injectable } from '@angular/core'
import { HttpClient } from '@angular/common/http'

@Injectable({
    providedIn: 'root'
})
export class ProductsService {
    constructor(private http: HttpClient) {

    }

    getAll() {
        return this.http.get(
            'https://getbootstrap.com/docs/4.0/components/buttons/'
        )
    }
}