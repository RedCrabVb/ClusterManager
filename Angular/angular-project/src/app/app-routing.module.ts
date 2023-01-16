import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { InitFileComponent } from './components/initfile/initfile.component';
import { AppComponent } from './app.component';

const routes: Routes = [
  {
    'path': '**', component: AppComponent
  }, 
  {
    'path': 'initfile', component: InitFileComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
