import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { InitFilePage } from './page/initfile/initfile.page.component';
import { WelcomeComponent } from './page/welcome/welcom.page.component';
import { HostsComponent } from './page/hosts/hosts.page';
import { ClusterComponenet } from './page/cluster/cluster.page';
import { LoginComponent } from './page/login/login.page.component';
import { AuthGuard } from './services/AuthGuard';

const routes: Routes = [
  {
    'path': 'initfile', component: InitFilePage, canActivate: [AuthGuard]
  },
  {
    'path': '', component: WelcomeComponent, canActivate: [AuthGuard]
  },
  {
    'path': 'hosts', component: HostsComponent, canActivate: [AuthGuard]
  },
  {
    'path': 'cluster', component: ClusterComponenet, canActivate: [AuthGuard]
  },
  {
    'path': 'login', component: LoginComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
