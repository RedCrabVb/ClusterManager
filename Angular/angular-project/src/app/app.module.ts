import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {PrductComponent} from './components/product/product.component'
import {NgbModule} from '@ng-bootstrap/ng-bootstrap';
// import { InitFileService } from './services/InitFile.service';
import { HttpClientModule } from '@angular/common/http'; 
import { AppHeaderComponent } from './components/header/app-header';
import { RouterModule, Routes } from '@angular/router';
import { InitFileComponent } from './components/initfile/initfile.component';

const routes: Routes = [
  {
    'path': '**', component: AppComponent
  }, 
  {
    'path': 'initfile', component: InitFileComponent
  }
];

@NgModule({
  declarations: [
    AppComponent,
    PrductComponent,
    AppHeaderComponent
  ],
  imports: [
    AppRoutingModule,
    BrowserModule,
    RouterModule.forRoot(routes),
    HttpClientModule,
    NgbModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
