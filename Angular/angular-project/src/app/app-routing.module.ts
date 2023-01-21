import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { InitFilePage } from './page/initfile/initfile.page.component';
import { WelcomeComponent } from './page/welcome/welcom.page.component';
import { HostsComponent } from './page/hosts/hosts.page';
import { ClusterComponenet } from './page/cluster/cluster.page';

const routes: Routes = [
  // {
    // 'path': '**', component: AppComponent
  // }, 
  {
    'path': 'initfile', component: InitFilePage
  },
  {
    'path': 'welcome', component: WelcomeComponent
  },
  {
    'path': 'hosts', component: HostsComponent
  },
  {
    'path': 'cluster', component: ClusterComponenet
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
