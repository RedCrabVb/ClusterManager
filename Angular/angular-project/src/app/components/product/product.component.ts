import { Component, Input } from "@angular/core";
import { IProduct } from "src/app/date/IProduct";

@Component({
    selector: 'app-product',
    templateUrl: './product.component.html'
})
export class PrductComponent{
    state: string = 'aborodai product'
    @Input() product: IProduct 

    description = false
}