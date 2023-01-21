import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { HttpClientModule } from '@angular/common/http'; 
import { AppHeaderComponent } from './components/header/app-header';
import { InitFilePage } from './page/initfile/initfile.page.component';
import { ModalComponent } from './components/modal/modal.component';
import { ModalService } from './components/modal/modalService';
import { HostsComponent } from './page/hosts/hosts.page';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ClusterComponenet } from './page/cluster/cluster.page';


@NgModule({
  declarations: [
    AppComponent,
    AppHeaderComponent, 
    ModalComponent,
    ClusterComponenet,
    HostsComponent,
    InitFilePage
  ],
  imports: [
    AppRoutingModule,
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    NgbModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
