import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { PrductComponent } from './components/product/product.component'
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { HttpClientModule } from '@angular/common/http'; 
import { AppHeaderComponent } from './components/header/app-header';
import { InitFilePage } from './page/initfile/initfile.page.component';
import { ModalComponent } from './components/modal/modal.component';
import { ModalService } from './components/modal/modalService';


@NgModule({
  declarations: [
    AppComponent,
    PrductComponent,
    AppHeaderComponent, 
    ModalComponent,
    InitFilePage
  ],
  imports: [
    AppRoutingModule,
    BrowserModule,
    HttpClientModule,
    NgbModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
