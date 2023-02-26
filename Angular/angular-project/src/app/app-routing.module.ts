import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { InitFilePage } from './page/initfile/initfile.page.component';
import { WelcomeComponent } from './page/welcome/welcom.page.component';
import { HostsComponent } from './page/hosts/hosts.page';
import { ClusterComponenet } from './page/cluster/cluster.page';
import { LoginComponent } from './page/login/login.page.component';
import { AuthGuard } from './services/AuthGuard';
import { ProcComponent } from './page/proc/proc.page.component';
import { PrototypeInitFileService } from './services/prototype_initfile.service';
import { PrototypeInitfileComponent } from './page/create_initfile/PrototypeInitfile.page.component';
import { EditorComponent } from './components/editor/editor.component';

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
  },
  {
    'path': 'proc_status', component: ProcComponent
  },
  {
    'path': 'initfile_create', component: PrototypeInitfileComponent
  },
  {
    'path': 'test', component: EditorComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
